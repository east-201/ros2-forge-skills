# Scan Delta Append Schema

Accepted fixes that change ROS2 public surface should append to the latest scan session:

```text
docs/ros2-quality/<LATEST_SCAN_RUN_ID>-scan/99_CHANGE_LOG_FROM_FIXES.md
```

The next `/ros2-scan` reads this file as previous context and writes a fresh scan session with `10_SCAN_DELTA_FROM_PREVIOUS.md`.
