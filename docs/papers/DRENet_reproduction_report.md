# DRENet 复现报告

**完成日期：** 2026-09-19  
**复现状态：** 已完成训练与独立测试集评估

## 1. 论文信息

- **题目：** A Degraded Reconstruction Enhancement-based Method for Tiny Ship Detection in Remote Sensing Images with A New Large-scale Dataset
- **作者：** Jianqi Chen, Keyan Chen, Hao Chen, Zhengxia Zou, Zhenwei Shi
- **期刊：** IEEE Transactions on Geoscience and Remote Sensing, 2022
- **代码：** https://github.com/WindVChen/DRENet
- **数据集：** https://github.com/WindVChen/LEVIR-Ship

## 2. 研究问题与方法

论文面向中分辨率遥感图像中的微小船舶检测。船舶目标像素少，易受海浪、云层和复杂背景干扰。

DRENet 基于 YOLOv5s，包含三项核心设计：

1. **DRE**：训练时以选择性退化图像作为辅助重建目标，引导网络关注船舶区域；推理时移除，不增加推理成本。
2. **CRMA**：以跨阶段多头注意力替换部分 CSP bottleneck，增强特征表达。
3. **Selective Degradation**：距离船舶更近的区域更清晰，背景区域退化更强，以降低背景干扰。

## 3. 数据集与划分

本次使用 LEVIR-Ship 数据集。`data/ship.yaml` 中的划分如下：

```yaml
train: D:/wonbin/datasets/LEVIR-Ship/train/images
val: D:/wonbin/datasets/LEVIR-Ship/val/images
test: D:/wonbin/datasets/LEVIR-Ship/test/images
nc: 1
names: ['ship']
```

训练过程使用验证集选择最佳权重；最终使用单独创建的 `data/ship_test.yaml` 在测试集评估。

## 4. 实验环境

| 项目 | 配置 |
|---|---|
| 操作系统 | Windows 10 22H2 |
| GPU | NVIDIA RTX 4000 Ada Generation，20 GB |
| CUDA 驱动报告版本 | 13.2 |
| Python | 3.8.20 |
| PyTorch | 2.1.0+cu118 |
| Conda 环境 | `drenet_wonbin` |
| 项目路径 | `D:/wonbin/projects/DRENet` |

为兼容 PyTorch 2.1，完成如下修改：

- `utils/datasets.py` 中 3 处 `astype(np.int)` 改为 `astype(int)`。
- `utils/general.py` 中 `astype(np.int)` 改为 `astype(int)`。
- `utils/loss.py` 中相关索引截断逻辑改为 `torch.clamp(gj, 0, int(gain[3] - 1)).long()`。

训练环境变量：

```bat
set CUDA_VISIBLE_DEVICES=1
set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

## 5. 训练配置

`runs/exp11/opt.yaml` 表明实际加载的是 DRENet 配置，而不是默认 YOLO 配置。

| 配置项 | 值 |
|---|---|
| 模型配置 | `./models/DRENet.yaml` |
| 数据配置 | `./data/ship.yaml` |
| 初始化权重 | 空，`weights: ''`，从头训练 |
| 输入尺寸 | 512 x 512 |
| batch size | 4 |
| epochs | 500 |
| 设备 | GPU 0，即 RTX 4000 Ada |
| 最佳权重 | `runs/exp11/weights/best.pt` |

训练命令：

```bat
python train.py --epochs 500 --batch-size 4 --device 0 --project ./runs --data ./data/ship.yaml
```

## 6. 实验结果

### 6.1 验证集最佳结果

500 epochs 训练约耗时 14 小时。训练过程记录的最佳验证集指标如下：

| 指标 | 值 |
|---|---:|
| Precision | 0.457 |
| Recall | 0.838 |
| mAP@0.5 | 0.763 |
| mAP@0.5:0.95 | 0.294 |
| box loss | 0.0448 |
| objectness loss | 0.0082 |

### 6.2 独立测试集复核

使用 `runs/exp11/weights/best.pt` 和 `data/ship_test.yaml` 对测试集进行独立评估：

```bat
python test.py --weights .\runs\exp11\weights\best.pt --batch-size 4 --device 0 --data .\data\ship_test.yaml --project .\runs\test_recheck --name drenet_test_500e_bs4
```

共评估 788 张图像、552 个船舶目标，耗时约 12 分钟。

| 指标 | 测试集结果 |
|---|---:|
| Precision | 0.600 |
| Recall | 0.871 |
| mAP@0.5 | 0.822 |
| mAP@0.5:0.95 | 0.272 |

### 6.3 与论文对比

| 指标 | 论文报告值 | 本次测试集结果 | 差异 |
|---|---:|---:|---:|
| mAP@0.5 | 0.824 | 0.822 | -0.002 |

测试集 mAP@0.5 与论文相差 0.2 个百分点，结果接近。训练轮数、batch size、随机性、PyTorch 版本和兼容性修改均可能造成细微差异。

## 7. 可视化问题说明

测试过程中的 `utils/plots.py` 后台绘图线程出现 OpenCV `cv2.putText` 断言错误，位置与批量绘制检测结果图有关。该异常没有中断评估：测试完成 197/197，最终指标和结果目录已生成。

因此数值评估结果有效；后续将单独修复绘图时的图像数据类型或位深问题，并补充批量可视化结果。

## 8. 结论与下一步

本次已完成 DRENet 的训练级复现：

- 作者提供的推理流程已跑通；
- 使用 `DRENet.yaml` 完成 500 epochs 从头训练；
- 使用 `best.pt` 完成独立测试集复核；
- 测试集 mAP@0.5 为 0.822，接近论文的 0.824。

下一步：

1. 在相同数据划分、输入尺寸、batch size 和训练轮数下训练 YOLOv5s 基线。
2. 修复批量绘图报错，整理正确检测、漏检和误检案例。
3. 先将稳定的 YOLO 基线接入 ShipVision 平台，再将 DRENet 作为可切换模型接入。

## 9. 结果文件位置

| 内容 | 路径 |
|---|---|
| 训练目录 | `D:/wonbin/projects/DRENet/runs/exp11` |
| 最佳权重 | `D:/wonbin/projects/DRENet/runs/exp11/weights/best.pt` |
| 测试复核结果 | `D:/wonbin/projects/DRENet/runs/test_recheck/drenet_test_500e_bs4` |
| 本报告 | `D:/projects/ship-vision-system/docs/papers/DRENet_reproduction_report.md` |
