# Design Intake Schema

`/ros2-design` must start with context reading, intake, and questions.

```text
Known requirements:
Known constraints:
Context already confirmed from source/docs/latest scan:
Unknown but important decisions:
P0 blocking questions:
P1 quality questions:
P2 future/backlog questions:
Assumptions:
Readiness: intake-needed / questions-sent / provisional-only / design-draft / design-review-failed / design-ready / superseded
```

Question count has no hard limit. The agent should ask as many useful questions as design correctness requires, grouped by P0/P1/P2. If there are many questions, ask P0 first and keep P1/P2 in the intake document.

A final architecture should only be written when readiness is `design-draft` and then accepted only after post-design review marks it `design-ready`, or when the user explicitly allows a provisional design with assumptions.
