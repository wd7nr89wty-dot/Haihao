from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG = logging.getLogger("haihao.dem.worker")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class WorkerConfig:
    worker_id: str
    workspace_root: Path
    gaea_executable: Path
    poll_seconds: int = 30

    @classmethod
    def load(cls, path: Path) -> "WorkerConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        root = os.path.expandvars(data.get("workspaceRoot", "%TEMP%/haihao-dem"))
        return cls(
            worker_id=data["workerId"],
            workspace_root=Path(root),
            gaea_executable=Path(os.path.expandvars(data["gaea"]["executable"])),
            poll_seconds=int(data.get("pollSeconds", 30)),
        )


class CloudAdapter:
    """Storage/queue boundary. Replace LocalCloudAdapter with R2/S3 adapter later."""

    def claim_next_job(self, worker_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def set_job_state(self, job: dict[str, Any], state: str, **fields: Any) -> None:
        raise NotImplementedError

    def download_job_inputs(self, job: dict[str, Any], workspace: Path) -> None:
        raise NotImplementedError

    def upload_build(self, job: dict[str, Any], output_dir: Path) -> None:
        raise NotImplementedError


class LocalCloudAdapter(CloudAdapter):
    """Development adapter using a local queue directory."""

    def __init__(self, root: Path):
        self.root = root
        self.queue = root / "queue"
        self.queue.mkdir(parents=True, exist_ok=True)

    def _job_path(self, job: dict[str, Any]) -> Path:
        return self.queue / f"{job['jobId']}.json"

    def claim_next_job(self, worker_id: str) -> dict[str, Any] | None:
        for path in sorted(self.queue.glob("*.json")):
            job = json.loads(path.read_text(encoding="utf-8"))
            if job.get("state") == "queued":
                job["state"] = "claimed"
                job["claimedBy"] = worker_id
                job["claimedAt"] = utc_now()
                path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
                return job
        return None

    def set_job_state(self, job: dict[str, Any], state: str, **fields: Any) -> None:
        job["state"] = state
        job.update(fields)
        self._job_path(job).write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")

    def download_job_inputs(self, job: dict[str, Any], workspace: Path) -> None:
        source = self.root / "projects" / job["projectId"]
        if source.exists():
            shutil.copytree(source, workspace / "project", dirs_exist_ok=True)

    def upload_build(self, job: dict[str, Any], output_dir: Path) -> None:
        target = self.root / "builds" / job["projectId"] / job["jobId"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(output_dir, target, dirs_exist_ok=True)


def run_gaea(config: WorkerConfig, job: dict[str, Any], workspace: Path, output_dir: Path) -> None:
    graph_name = job["gaea"]["graphFile"]
    matches = list(workspace.rglob(graph_name))
    if not matches:
        raise FileNotFoundError(f"GAEA graph not found: {graph_name}")
    graph = matches[0]
    output_dir.mkdir(parents=True, exist_ok=True)

    # GAEA command-line arguments can differ by installed GAEA version.
    # Override the full command with HAIHAO_GAEA_COMMAND until the installed CLI is verified.
    template = os.getenv("HAIHAO_GAEA_COMMAND")
    if not template:
        raise RuntimeError("Set HAIHAO_GAEA_COMMAND after verifying the installed GAEA CLI syntax")
    command = template.format(exe=str(config.gaea_executable), graph=str(graph), output=str(output_dir))
    LOG.info("Starting GAEA build for %s", job["jobId"])
    subprocess.run(command, shell=True, check=True, cwd=workspace, timeout=int(job["gaea"].get("timeoutMinutes", 240)) * 60)


def create_build_manifest(config: WorkerConfig, job: dict[str, Any], output_dir: Path) -> Path:
    files = []
    for path in sorted(output_dir.rglob("*")):
        if path.is_file():
            files.append({
                "path": path.relative_to(output_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    manifest = {
        "schemaVersion": "0.1.0",
        "jobId": job["jobId"],
        "projectId": job["projectId"],
        "workerId": config.worker_id,
        "completedAt": utc_now(),
        "files": files,
    }
    path = output_dir / "build-manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def process_job(config: WorkerConfig, cloud: CloudAdapter, job: dict[str, Any]) -> None:
    workspace = config.workspace_root / job["jobId"]
    output_dir = workspace / "output"
    try:
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True)
        cloud.set_job_state(job, "downloading", updatedAt=utc_now())
        cloud.download_job_inputs(job, workspace)
        cloud.set_job_state(job, "building", updatedAt=utc_now())
        run_gaea(config, job, workspace, output_dir)
        create_build_manifest(config, job, output_dir)
        cloud.set_job_state(job, "uploading", updatedAt=utc_now())
        cloud.upload_build(job, output_dir)
        cloud.set_job_state(job, "completed", completedAt=utc_now())
    except Exception as exc:
        LOG.exception("Job %s failed", job.get("jobId"))
        cloud.set_job_state(job, "failed", failedAt=utc_now(), errorMessage=str(exc))
    finally:
        if job.get("cleanup", {}).get("deleteWorkspaceAfterUpload", True):
            shutil.rmtree(workspace, ignore_errors=True)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config_path = Path(os.getenv("HAIHAO_WORKER_CONFIG", "worker.json"))
    config = WorkerConfig.load(config_path)
    config.workspace_root.mkdir(parents=True, exist_ok=True)
    local_cloud_root = Path(os.getenv("HAIHAO_LOCAL_CLOUD", str(Path(tempfile.gettempdir()) / "haihao-dem-cloud")))
    cloud: CloudAdapter = LocalCloudAdapter(local_cloud_root)
    LOG.info("Worker %s online", config.worker_id)
    while True:
        job = cloud.claim_next_job(config.worker_id)
        if job:
            process_job(config, cloud, job)
        else:
            time.sleep(config.poll_seconds)


if __name__ == "__main__":
    sys.exit(main())
