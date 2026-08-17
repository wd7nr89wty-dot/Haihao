# PSAR 二战飞机生产线

当前线上引导版本：0.6.0

首架验证机：B-24 Liberator

核心协议：Progressive Semantic Aircraft Rig，简称 PSAR。

## 系统原则

1. 整架飞机持续使用同一份权威 GLB，不切换传统网格 LOD。
2. 飞机加载时一次创建完整语义节点。镜头放大后逐级显露机体、功能系统、机械机构和生产解剖信息。
3. 生命周期统一覆盖停放、启动、暖机、滑行、试车、起飞、爬升、巡航、下降、进近、着陆、滑回和停机。
4. 每台发动机拥有独立状态、烟雾、热扰动、声音、故障和火灾锚点。
5. 飞机、技能和依赖通过签名注册表、不可变版本路径、SHA-256、缓存、暂存、回滚和安全重载进行管理。
6. OpenPBR、glTF 2.0 KHR 扩展、Three.js WebGPU、物理景深、无降噪路径追踪接口均属于统一渲染协议。

## B-24 v1.2.0

当前 B-24 数据包包含 104 个语义节点、5 个渐进等级、16 个生产工序、22 个运行阶段、4 台独立发动机和 10 类签名资源。模型仍为一份不可变 GLB。在线传输支持完整对象与 6 个逐块校验的恢复分块。

## 当前分支用途

`agent/psar-v0.6-bootstrap` 用于把 PSAR 注册表、机型数据、技能和依赖接入现有 Haihao 多生产线仓库。现有 `architecture-pipeline` 与 `dem-pipeline` 不受影响。

23,085,972 字节的 B-24 GLB 与二进制恢复分块需要通过项目自带的认证发布脚本或 Cloudflare R2 工作流上传。发布私钥不得提交到仓库。

## 版本锁

```text
Application                 0.6.0
B-24 package                1.2.0
Aircraft production skill   1.2.0
Dependency lock             2026.08.18.1
Three.js                    0.185.1
img2threejs commit          d6673386f89673a58736f8d398dd16ece67874f5
```
