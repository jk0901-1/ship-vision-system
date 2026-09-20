\# DRENet 复现记录



\## 当前状态

\- 已完成：

&#x20; - 环境配置（RTX 4000 Ada、PyTorch 2.1）

&#x20; - 500 epochs 训练，mAP 76.3

&#x20; - 1000 epochs 训练，mAP 78.4

&#x20; - 推理跑通

\- 正在进行：

&#x20; - 项目工程化

\- 未完成：

&#x20; - ONNX 导出

&#x20; - TensorRT 加速

\- 当前阻塞：

&#x20; - 无



\## 环境

\- 系统：Windows 10

\- Python：3.8.20

\- PyTorch：2.1.0+cu118

\- CUDA：11.8

\- GPU：RTX 4000 Ada 20GB

\- DRENet 代码：GitHub WindVChen/DRENet

\- 数据集：LEVIR-Ship（2320/788/788）



\## 下一步验证

\- \[ ] 跑通作者权重推理

\- \[ ] 保存 10 张检测可视化结果

\- \[ ] 记录 AP、推理耗时





\## 2026-09-20 进展



\- \[x] 创建 feature/platform-foundation 分支

\- \[x] 建项目目录结构

\- \[x] 写 project\_scope.md、reproduction\_log.md、drenet\_setup.md

\- \[x] 导出 ONNX：drenet.onnx（20.1 MB）

\- \[x] 下载 ONNX 到本地 models/

\- \[ ] 本地 ONNX Runtime 测试推理

