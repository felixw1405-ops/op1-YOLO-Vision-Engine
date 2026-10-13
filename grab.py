import mss, cv2, numpy as np, time, os
os.makedirs("shots", exist_ok=True)
with mss.mss() as s:
    mon = s.monitors[1]   # 1 = main display, 2 = second monitor
    i = 0
    print("Capturing every 1s. Ctrl+C to stop.")
    time.sleep(5)         # 5 seconds to switch to your game
    while True:
        img = np.array(s.grab(mon))
        cv2.imwrite(f"shots/{i:05d}.jpg", img[:, :, :3])
        i += 1
        time.sleep(1)
