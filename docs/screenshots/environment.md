# 环境配置说明

## 硬件
- 电脑：DELL
- GPU：Intel Iris Xe 核显（无 NVIDIA 独立显卡）
- 训练方式：本地 CPU 调试 + 实验室学习机训练

## 软件
- OS: Windows 10.0.26200
- Miniconda: 3.0.4
- Python: 3.10（shipvision 环境）
- PyTorch: 2.14.0+cpu
- Git: 2.55.0（安装于 E:\Git）

## 验证
- torch.cuda.is_available() = False（正常，无N卡）
- 矩阵乘法测试通过

## 复现步骤
1. conda create -n shipvision python=3.10 -y
2. conda activate shipvision
3. pip install -r requirements.txt

## 训练平台
- 本地：CPU，仅用于调试和小数据
- 实验室学习机：待师兄配置