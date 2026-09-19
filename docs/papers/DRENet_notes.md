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













\## 2026-09-17 复现进度



\### 工作站

\- 系统：Windows 10 22H2

\- GPU：NVIDIA T400 4GB + RTX 4000 Ada 20GB

\- CUDA：13.2

\- conda 根目录：D:\\anconda3（拼写少一个a）

\- 环境：D:\\anconda3\\envs\\drenet\_wonbin

\- Python 3.8.20 + PyTorch 2.1.0+cu118



\### 项目路径

\- 代码：D:\\wonbin\\projects\\DRENet\\

\- 数据：D:\\wonbin\\datasets\\LEVIR-Ship\\

\- 权重：D:\\wonbin\\weights\\DRENet.pt

\- 结果：D:\\wonbin\\projects\\DRENet\\runs\\detect\\exp\\



\### 已完成

\- \[x] 推理跑通（788 张，35 秒）

\- \[x] 结果检查正常（正样本有框，负样本无框）



\### 下一步

\- \[ ] train.py 短训练（10 epochs）

\- \[ ] 正式训练 500-1000 epochs

\- \[ ] 复现报告













\## 2026-09-18 训练跑通



\### 解决的兼容性问题（PyTorch 2.1）

1\. `utils/datasets.py`: `astype(np.int)` → `astype(int)`（3处）

2\. `utils/general.py`: `astype(np.int)` → `astype(int)`

3\. `utils/loss.py`: `clamp` 用 `torch.clamp(gj, 0, int(gain\[3]-1)).long()`



\### 运行配置

\- GPU: RTX 4000 Ada（`CUDA\_VISIBLE\_DEVICES=1`）

\- batch-size: 4

\- 环境变量: `PYTORCH\_CUDA\_ALLOC\_CONF=expandable\_segments:True`



\### 训练命令

```bash

python train.py --epochs 500 --batch-size 4 --device 0 --project ./runs --data ./data/ship.yaml






## 2026-09-19 复现结果

### 500 epochs 完成（约 14 小时）

| 指标 | 值 |
|---|---|
| mAP@0.5 | 0.763 |
| mAP@0.5:0.95 | 0.294 |
| Precision | 0.457 |
| Recall | 0.838 |
| box_loss | 0.0448 |
| obj_loss | 0.0082 |

### 与论文对比
| 指标 | 论文 | 复现 | 差异 |
|---|---|---|---|
| mAP@0.5 | 82.4 | 76.3 | -6.1 |

### 差异原因
1. Batch size: 4 vs 16
2. Epochs: 500 vs 1000
3. GPU: RTX 4000 Ada vs V100

### 混淆矩阵
- 83% 船舶正确检测
- 17% 漏检
- 背景误检较多（Precision 0.457）

### 结论
合格复现，差距合理。

