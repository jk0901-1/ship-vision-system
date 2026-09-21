import onnxruntime as ort
import numpy as np
import cv2
import os

model_path = 'D:/projects/ship-vision-system/models/drenet.onnx'

print('Loading ONNX model...')
session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
print('Model loaded')

print('Inputs:', [(i.name, i.shape) for i in session.get_inputs()])
print('Outputs:', [(o.name, o.shape) for o in session.get_outputs()])

# 用随机图测试
img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
img = img.transpose(2, 0, 1).astype(np.float32) / 255.0
img = np.expand_dims(img, 0)

print('Running inference...')
input_name = session.get_inputs()[0].name
outputs = session.run(None, {input_name: img})
print(f'Output shape: {outputs[0].shape}')
print('Inference OK')