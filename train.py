from ultralytics import YOLO

model = YOLO("models/v4.5_best.pt")

model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    device="mps",
    workers=8,
    cache=True,
    patience=30,
    project="runs/detect",
    name="v5"
)
