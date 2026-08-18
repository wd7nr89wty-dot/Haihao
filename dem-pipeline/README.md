# DEM 地图生产线

云端优先的 DEM 地形生产系统。目标是把项目配置、原始 DEM、核心区增强数据、GAEA 构建任务、版本信息和 Three.js 网页成果统一纳入可追踪的在线生产流程。

## 当前桂林成果

- Public Viewer: https://wd7nr89wty-dot.github.io/Haihao/
- GAEA Proof: https://wd7nr89wty-dot.github.io/Haihao/guilin/gaea-proof/
- Legacy Viewer: https://guilin-dem-terrain.sunhaihao.chatgpt.site
- Legacy GAEA Proof: https://guilin-dem-terrain.sunhaihao.chatgpt.site/guilin/gaea-proof

## 已确定生产规则

1. 每个项目覆盖约 5000 km²。
2. 桂林全域统一采用用户确认的公开免费 12.5 m DEM 作为基础高程。
3. 指定核心地点周围设置 36 km² 核心区。
4. 核心区继续寻找许可可用且原生分辨率优于 12.5 m 的免费 DEM。
5. 无更高分辨率数据时，以全域 12.5 m DEM 为基础，结合真实河道、机场、稻田、喀斯特等地貌约束进入增强流程。
6. 12.5 m 像元间距与源 DEM 谱系分别登记，下载文件的 README、GeoTIFF 元数据和处理记录进入构建清单。
7. GAEA 在私有 Windows Worker 后台运行。Worker 只保留临时缓存，完成后上传成果并清理本地任务数据。
8. Three.js / WebGPU 负责在线检查、成果展示与后续项目整合。

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

- 登记实际下载的 12.5 m DEM 文件名、GeoTIFF 元数据和来源 README
- 上传桂林 5000 km² DEM 到对象存储
- 建立河道、机场、稻田和喀斯特语义掩膜
- 接入 GAEA Windows Worker 与构建状态 API
- 发布第一份真实 `Z_truth`、`Z_render`、`Z_collision`、`Z_delta` 和 `detail_confidence`
