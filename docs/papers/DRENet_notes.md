\# DRENet 复现笔记



\## 论文

\- 标题：A Degraded Reconstruction Enhancement-Based Method for Tiny Ship Detection in Remote Sensing Images With a New Large-Scale Dataset

\- 作者：Jianqi Chen et al.（北航）

\- 期刊：IEEE TGRS 2022

\- 代码：https://github.com/WindVChen/DRENet

\- 数据集：https://github.com/WindVChen/LEVIR-Ship



\## 环境

\- Python 3.8

\- PyTorch 1.9.0

\- wandb（可选）



\## 核心

\- DRE：训练时重建模糊图，推理时删掉

\- CRMA：替换 YOLOv5 的 CSP bottleneck

\- Selective Degradation：按到船舶距离决定模糊程度



\## 本地路径

\- 代码：D:\\projects\\DRENet\\

\- 数据：D:\\datasets\\LEVIR-Ship\\

\- 权重：D:\\projects\\DRENet\\weights\\DRENet.pt



\## 进度

\- \[x] 准备代码+数据+权重

\- \[x] 改 ship.yaml

\- \[ ] 连工作站

\- \[ ] 跑推理

\- \[ ] 跑训练

\- \[ ] 写复现报告



\## 明天任务

\- 找老师/师兄要工作站信息

\- MobaXterm 试连

\- nvidia-smi 看 CUDA 版本

\- 建 drenet 环境，装 PyTorch 1.9.0

