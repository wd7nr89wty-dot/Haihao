# Windows GAEA Worker Protocol v0.1

## 目标

Windows Worker 是 DEM 云端生产线中唯一需要安装 GAEA 的执行节点。项目源数据、配置、图文件、构建记录和正式成果均以云端版本为准。本机仅保存一次构建所需的临时工作区。

## Worker 生命周期

1. Worker 启动并生成唯一 `workerId`。
2. 检查云端任务队列。
3. 领取一个 `queued` Job，将状态更新为 `claimed`。
4. 创建 `%TEMP%/haihao-dem/<jobId>/` 临时工作区。
5. 下载 Job 指定的 project manifest、GAEA graph 与输入资产。
6. 校验输入文件完整性，状态更新为 `downloading` 后进入 `building`。
7. 调用本机 GAEA 执行指定 Graph。
8. 收集高度图、mask、日志以及构建元数据。
9. 生成 `build-manifest.json`，记录输入版本、Worker、GAEA 版本、输出文件及校验值。
10. 状态更新为 `uploading`，将成果上传到 Job 的 `uploadPrefix`。
11. 云端确认必需成果存在后，将 Job 标记为 `completed`。
12. 删除整个本地临时工作区。

## 失败策略

任何阶段失败都必须把 Job 标记为 `failed`，并记录：

- failureStage
- errorCode
- errorMessage
- workerId
- timestamp
- build log

失败任务可以保留日志，DEM、纹理、中间缓存和 GAEA 临时文件仍应清理。

## Worker 不应长期保存

- 原始 DEM
- GAEA Graph 的唯一正式副本
- 项目 JSON 的唯一正式副本
- 构建后的正式高度图
- 正式纹理和 mask

## 状态机

```text
queued
  -> claimed
  -> downloading
  -> building
  -> uploading
  -> completed

任意执行状态 -> failed
queued/claimed -> cancelled
```

## 并发原则

第一阶段每台 Worker 同时执行 1 个 GAEA Job。后续根据显存、内存、CPU 和 GAEA 实际稳定性再开放并发。

## 安全原则

Worker 凭据通过环境变量或系统凭据存储提供，禁止写入 Git 仓库。上传权限应限制到 DEM Pipeline 所需的云端路径。
