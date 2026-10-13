import cv2, sys, time, numpy as np, mss
from ultralytics import YOLO

weights = sys.argv[1] if len(sys.argv) > 1 else "yolov8n.pt"
source  = sys.argv[2] if len(sys.argv) > 2 else "screen"   # "screen" or a video file
MONITOR = 1          # monitor with the game (1 = main, 2 = second)
conf    = 0.35
model   = YOLO(weights)

def frames():
    if source == "screen":
        with mss.mss() as s:
            mon = s.monitors[MONITOR]
            while True:
                yield np.array(s.grab(mon))[:, :, :3].copy()
    else:
        cap = cv2.VideoCapture(source)
        while True:
            ok, f = cap.read()
            if not ok:
                break
            yield f

fps, last, n = 0, time.time(), 0
for frame in frames():
    t0 = time.time()
    res = model(frame, imgsz=640, conf=conf, device="mps", verbose=False)[0]
    ms = (time.time() - t0) * 1000
    view = res.plot()                       # boxes + labels + confidence

    h, w = view.shape[:2]
    cv2.drawMarker(view, (w // 2, h // 2), (0, 255, 255), cv2.MARKER_CROSS, 20, 2)  # screen center
    for b in res.boxes.xywh.cpu().numpy():   # line from center to each detection
        cv2.line(view, (w // 2, h // 2), (int(b[0]), int(b[1])), (0, 255, 255), 1)

    n += 1
    if time.time() - last >= 1:
        fps, n, last = n, 0, time.time()
    cv2.putText(view, f"{fps} fps | {ms:.0f} ms | {len(res.boxes)} det | conf>{conf:.2f}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    view = cv2.resize(view, (1280, int(1280 * h / w)))   # fit the window
    cv2.imshow("model view", view)
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"): break
    if k == ord("s"): cv2.imwrite(f"debug_{int(time.time())}.jpg", view)
    if k == ord("="): conf = min(conf + 0.05, 0.95)
    if k == ord("-"): conf = max(conf - 0.05, 0.05)
cv2.destroyAllWindows()
