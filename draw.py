import cv2


def draw(frame, detections):
    """
    Draw tracked detections onto the frame, including track IDs.
    """

    for detection in detections:

        x1, y1, x2, y2 = detection["box"]
        confidence = detection["confidence"]
        track_id = detection.get("track_id", -1)
        cls = detection.get("class", 0)

        # How many frames this track has been missing
        missing = detection.get("missing", 0)

        # Choose color based on tracker state
        if missing == 0:
            color = (0, 255, 0)      # Green
        elif missing <= 2:
            color = (0, 255, 255)    # Yellow
        elif missing <= 4:
            color = (0, 165, 255)    # Orange
        else:
            color = (0, 0, 255)      # Red

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Build label with ID, class, and confidence
        label = f"ID:{track_id} | {confidence:.2f}"
        if missing > 0:
            label += f" | M:{missing}"

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    return frame
