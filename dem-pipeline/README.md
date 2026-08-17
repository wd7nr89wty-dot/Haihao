# DEM 地图生产线

云端优先的 DEM 地形生产系统。目标是把项目配置、原始 DEM、核心区增强数据、GAEA 构建任务、版本信息和 Three.js 网页成果统一纳入可追踪的在线生产流程。

## 当前桂林成果

- Web Viewer: https://guilin-dem-terrain.sunhaihao.chatgpt.site
- GAEA Proof: https://guilin-dem-terrain.sunhaihao.chatgpt.site/guilin/gaea-proof

## 已确定生产规则

1. 每个项目覆盖约 5000 km²。
2. 全域统一采用公开免费的约 13 m DEM 作为基础高程。
3. 指定核心地点周围设置 36 km² 核心区。
4. 核心区优先寻找许可可用且原生分辨率优于 13 m 的免费 DEM。
5. 无更高分辨率数据时，以全域 DEM 为基础，结合真实河道、机场、稻田、喀斯特等地貌约束进入增强流程。
6. GAEA 在私有 Windows Worker 后台运行。Worker 只保留临时缓存，完成后上传成果并清理本地任务数据。
7. Three.js / WebGPU 负责在线检查、成果展示与后续项目整合。

## 云端目录约定

```text
projects/<project-id>/
  project.json
  sources/
    dem/
    vectors/
    imagery/
  gaea/
    graphs/
    builds/
  derived/
    terrain/
    textures/
    masks/
  web/
  manifests/
```

## 下一阶段

- 建立 project.schema.json
- 建立桂林项目 project.json
- 建立 GAEA job manifest
- 建立 Windows Worker 协议
- 建立发布 manifest 与版本回滚规则
- 将桂林作为第一条端到端样板生产线
