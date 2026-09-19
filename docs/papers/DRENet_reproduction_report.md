\# DRENet 复现报告



\## 1. 论文信息



\- \*\*标题\*\*：A Degraded Reconstruction Enhancement-Based Method for Tiny Ship Detection in Remote Sensing Images With a New Large-Scale Dataset

\- \*\*作者\*\*：Jianqi Chen, Keyan Chen, Hao Chen, Zhengxia Zou, Zhenwei Shi（北京航空航天大学）

\- \*\*期刊\*\*：IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2022

\- \*\*代码\*\*：https://github.com/WindVChen/DRENet

\- \*\*数据集\*\*：https://github.com/WindVChen/LEVIR-Ship



\## 2. 论文理解



\### 2.1 要解决的问题



中分辨率（16m/pixel）遥感图像中的微小船舶检测。船舶在图像中仅占 10×10 像素，纹理少、边缘模糊，且背景有大量碎云、海浪干扰。



\### 2.2 核心方法



\*\*DRENet 由三部分组成：\*\*



1\. \*\*Backbone\*\*：YOLOv5s 轻量骨干网络

2\. \*\*DRE（Degraded Reconstruction Enhancer）\*\*：

&#x20;  - 训练时重建"选择性退化"的模糊图

&#x20;  - 引导 backbone 关注船舶，忽略背景

&#x20;  - \*\*推理时删除\*\*，不增加推理成本

3\. \*\*Detector\*\*：

&#x20;  - 用 CRMA（跨阶段多头注意力）替换 CSP bottleneck

&#x20;  - 扩大感受野，提升小目标检测



\*\*Selective Degradation（选择性退化）\*\*：

\- 按像素到最近船舶的距离，决定模糊核大小

\- 离船越近越清晰，越远越模糊

\- 公式：`boxSize = (int(1.03^(minDis^0.5))) // 2`



\*\*Loss\*\*：

\- Enhancer Loss（MSE 重建误差）

\- Detector Loss（CIoU + BCE）

\- 自动权重平衡（可学习参数 a、b）



\### 2.3 实验结果（论文）



| 指标 | 值 |

|---|---|

| mAP@0.5 | 82.4 |

| FPS | 85 |

| Params | 4.79M |

| FLOPs | 8.3G |



\## 3. 复现过程



\### 3.1 环境配置



| 项目 | 配置 |

|---|---|

| 操作系统 | Windows 10 22H2 |

| GPU | NVIDIA RTX 4000 Ada Generation（20GB） |

| CUDA | 13.2 |

| Python | 3.8.20 |

| PyTorch | 2.1.0+cu118 |

| conda 环境 | drenet\_wonbin |



\*\*环境变量\*\*：

```bash

set CUDA\_VISIBLE\_DEVICES=1

set PYTORCH\_CUDA\_ALLOC\_CONF=expandable\_segments:True

