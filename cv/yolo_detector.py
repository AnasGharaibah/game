from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path='yolov8n.pt', confidence=0.6):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                conf = float(box.conf[0])
                if conf >= self.confidence:
                    cls = int(box.cls[0])
                    label = self.model.names[cls]
                    # box.xywh gives [x_center, y_center, width, height]
                    # but actually ultralytics often returns xyxy
                    # Let's use xyxy and convert or just use what we need
                    x1, y1, x2, y2 = box.xyxy[0]
                    bx, by, bw, bh = float(x1), float(y1), float(x2 - x1), float(y2 - y1)
                    detections.append({
                        'label': label,
                        'conf': conf,
                        'bbox': (bx, by, bw, bh)
                    })
        return detections
