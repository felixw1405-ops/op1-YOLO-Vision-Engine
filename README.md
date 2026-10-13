# Realtime Vision Engine

MACOS VERSION only for now because my windows pc broke😭

A low-latency, real-time computer vision pipeline in Python built on Ultralytics YOLO.
Its made around a rule: **always work on the newest data, and never let a slow
stage delay a fast one.** (Thats not a rule i just created one lmfaoooo).

> v5.2 is complete. Currently working on v5.3a (instrumentation).

## Design principles

- **Latency over completeness.** Intermediate frames are dropped on purpose.
- **Latest will always (i mean.. maybe) wins communication.** Stages share the newest value, not a backlog.
- **Immutable packets.** Published data is never mutated after publication.
- **Measure before optimizing.** Every stage is timestamped and observable.
- **Maintainability over peak accuracy.** Small, replaceable components with clear interfaces.

## Architecture

```literally how it works
Capture thread
      |  publishes FramePacket
      v
 latest_frame (AtomicReference)
      |
      v
DetectorWorker thread
      |  detect -> track
      v
 latest_tracks (AtomicReference)
      |
      v
Preview / renderer (independent loop)
```

- **Capture** publishes immutable `FramePacket`s.
- **DetectorWorker** consumes only the newest frame, runs detection, then tracking.
- **Renderer** draws the latest frame and latest tracks at its own rate and never waits on inference.

## Data model

| Packet | Purpose |
|---|---|
| `FramePacket` | Image plus `frame_id` and capture timestamp |
| `TrackPacket` | Tracks plus the capture timestamp of the frame they describe |
| `PredictionPacket` | Draw-ready boxes extrapolated to a display time |

All timestamps use a monotonic clock so stage ages can be compared safely.

## Requirements

- Python 3.10+
- [Ultralytics](https://docs.ultralytics.com/)
- OpenCV, NumPy
- A CUDA-capable GPU is recommended

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Add configuration details here (model path, input source, image size, thresholds).

## Observability

The engine reports per-stage timings so latency can be measured instead of guessed:

- Capture time
- Inference time
- Tracker time
- Frame age at display
- Pipeline age (capture to display)

Report percentiles (p50 / p95 / p99), not just instantaneous values.

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v5.2 | Threaded capture, DetectorWorker, shared packets, latest-frame pipeline | Done |
| v5.3a | Timestamps on every packet, latency metrics overlay, event-based wakeup, track TTL | Next |
| v5.3b | Render-side prediction (extrapolate to the displayed frame's timestamp), One Euro smoothing | Planned |
| v5.4 | ByteTrack, time-based `dt` and track lifetimes, Kalman tuning | Planned |
| v6 | Record/replay, plugin API, world state | Planned |

Changes are made one at a time and measured against a baseline so improvements can be
attributed to a specific cause.

## Known limitations

- Boxes can lag moving objects until timestamp alignment and prediction land (v5.3).
- Tracker parameters are currently frame-based, so behavior varies with load until v5.4.

## Contributing

Issues and pull requests are welcome. Please include before/after latency numbers
for any performance-related change.

## License

Add your license here.
