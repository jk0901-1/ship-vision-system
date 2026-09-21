import onnxruntime as ort
import numpy as np
import cv2
import time


class ONNXPredictor:
    def __init__(self, model_path: str, conf_thres: float = 0.25, iou_thres: float = 0.45):
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

    def preprocess(self, image_path: str, img_size: int = 512):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_size, img_size))
        img = img.transpose(2, 0, 1).astype(np.float32) / 255.0
        img = np.expand_dims(img, 0)
        return img

    def predict(self, image_path: str):
        img = self.preprocess(image_path)
        t0 = time.time()
        outputs = self.session.run(None, {self.input_name: img})
        inference_time = (time.time() - t0) * 1000  # ms
        detections = outputs[0]  # (1, 16128, 6)
        return detections, inference_time


if __name__ == '__main__':
    import os
    predictor = ONNXPredictor('D:/projects/ship-vision-system/models/drenet.onnx')
    sample_dir = 'D:/projects/ship-vision-system/outputs/drenet_samples'
    os.makedirs(sample_dir, exist_ok=True)
    test_img = os.path.join(sample_dir, 'test.png')
    if not os.path.exists(test_img):
        img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        cv2.imwrite(test_img, img)
    detections, t = predictor.predict(test_img)
    print(f'Detections shape: {detections.shape}')
    print(f'Inference time: {t:.2f} ms')