# Decision Review Task Placeholders

Prompt 45 defines review task placeholders for future Decision Desk human
review workflow planning.

## Schema

Each task placeholder has a stable task id, a task kind, a title, a
description, safety labels, schema version, creation timestamp, and notes.
Supported task kinds are evidence review, safety review, validation review,
display review, and final review placeholder.

## Safety Boundary

Task placeholders are not assigned tasks. They are not active tasks. They are
not completed tasks. They do not grant approvals, grant overrides, generate
recommendations, generate action states, compute confidence scores, generate
active DecisionObjects, generate readiness-to-trade, mark execution readiness,
or publish events.

The task placeholder contract exists so future prompts can discuss workflow
shape without introducing active workflow behavior.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
