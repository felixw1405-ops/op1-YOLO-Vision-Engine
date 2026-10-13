import torch
from ultralytics import YOLO


class Detector:
    def __init__(self):
        self.model = YOLO("models/v5_best.pt")

        # Small speed optimizations
        torch.set_grad_enabled(False)

    @torch.inference_mode()
    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            imgsz=512,
            conf=0.35,
            iou=0.45,
            verbose=False,
            augment=False,
            max_det=25
        )

        detections = []

        for result in results:

            boxes = result.boxes

            if boxes is None or len(boxes) == 0:
                continue

            xyxy = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy()
            classes = boxes.cls.cpu().numpy().astype(int)

            for box, conf, cls in zip(xyxy, confs, classes):

                detections.append({
                    "box": (
                        int(box[0]),
                        int(box[1]),
                        int(box[2]),
                        int(box[3])
                    ),
                    "confidence": float(conf),
                    "class": cls
                })

        return detections
