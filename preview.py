import cv2
import numpy as np
import time
from mss import mss

from detector import Detector
from tracker import Tracker
from draw import draw

# Initialize detector and tracker
detector = Detector()
tracker = Tracker()

# Screen capture
sct = mss()
monitor = sct.monitors[1]

last_time = time.perf_counter()
fps = 0

while True:

    # ---------- Capture ----------
    t0 = time.perf_counter()

    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    capture_ms = (time.perf_counter() - t0) * 1000

    # ---------- Detection ----------
    t0 = time.perf_counter()

    detections = detector.detect(frame)

    detect_ms = (time.perf_counter() - t0) * 1000

    # ---------- Tracker ----------
    t0 = time.perf_counter()

    tracks = tracker.update(detections)

    tracker_ms = (time.perf_counter() - t0) * 1000

    # ---------- Draw ----------
    t0 = time.perf_counter()

    frame = draw(frame, tracks)

    draw_ms = (time.perf_counter() - t0) * 1000

    # ---------- FPS ----------
    now = time.perf_counter()
    fps = 1 / (now - last_time)
    last_time = now

    # ---------- Overlay ----------
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Capture: {capture_ms:.1f} ms",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Detect: {detect_ms:.1f} ms",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Tracker: {tracker_ms:.2f} ms",
        (10, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Draw: {draw_ms:.2f} ms",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.imshow("YOLO Live Preview", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
