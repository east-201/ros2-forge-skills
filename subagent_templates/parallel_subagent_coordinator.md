# parallel-subagent-coordinator

Purpose: merge independent subagent lane outputs into one coherent ROS2 design/review/fix/verification decision.

Required inputs:
- Active session index
- Lane reports
- User requirements
- Latest scan/contract when available

Output:
- PARALLEL_LANE_SUMMARY.md
- CONFLICTS_AND_DEPENDENCIES.md
- MERGED_DECISION.md

Rules:
- Preserve conflicts; do not silently choose.
- Mark blocked/provisional/ready status.
- Do not edit source.
- Do not claim V5 without user evidence.
