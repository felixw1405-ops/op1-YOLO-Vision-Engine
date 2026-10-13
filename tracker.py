import math


def lerp(a, b, t):
    return a + (b - a) * t


class Track:
    def __init__(self, detection):
        self.box = detection["box"]
        self.confidence = detection["confidence"]
        self.cls = detection["class"]

        self.age = 0
        self.missing = 0


class Tracker:
    def __init__(self):
        self.tracks = []

        # Settings
        self.max_missing = 6
        self.match_distance = 75
        self.smoothing = 0.35

    def center(self, box):
        x1, y1, x2, y2 = box
        return (
            (x1 + x2) / 2,
            (y1 + y2) / 2
        )

    def distance(self, box1, box2):
        c1 = self.center(box1)
        c2 = self.center(box2)

        return math.hypot(
            c1[0] - c2[0],
            c1[1] - c2[1]
        )

    def smooth_box(self, old_box, new_box):
        return (
            int(lerp(old_box[0], new_box[0], self.smoothing)),
            int(lerp(old_box[1], new_box[1], self.smoothing)),
            int(lerp(old_box[2], new_box[2], self.smoothing)),
            int(lerp(old_box[3], new_box[3], self.smoothing)),
        )

    def update(self, detections):

        used = set()

        # Update existing tracks
        for track in self.tracks:

            best_index = None
            best_detection = None
            best_distance = self.match_distance

            for i, detection in enumerate(detections):

                if i in used:
                    continue

                d = self.distance(track.box, detection["box"])

                if d < best_distance:
                    best_distance = d
                    best_index = i
                    best_detection = detection

            if best_detection is not None:

                used.add(best_index)

                # Smooth movement
                track.box = self.smooth_box(
                    track.box,
                    best_detection["box"]
                )

                # Smooth confidence
                track.confidence = lerp(
                    track.confidence,
                    best_detection["confidence"],
                    0.30
                )

                track.cls = best_detection["class"]

                track.missing = 0
                track.age += 1

            else:

                track.missing += 1
                track.age += 1

        # Create new tracks
        for i, detection in enumerate(detections):

            if i not in used:
                self.tracks.append(Track(detection))

        # Remove expired tracks
        self.tracks = [
            track
            for track in self.tracks
            if track.missing <= self.max_missing
        ]

        # Return tracks
        output = []

        for track in self.tracks:

            output.append({
                "box": track.box,
                "confidence": track.confidence,
                "class": track.cls,
                "missing": track.missing,
                "age": track.age
            })

        return output
