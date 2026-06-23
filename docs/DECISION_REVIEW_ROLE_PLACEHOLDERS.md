# Decision Review Role Placeholders

Prompt 45 defines reviewer role placeholders for future Decision Desk human
review workflow planning.

## Schema

Each reviewer role placeholder has a role id, role kind, display name,
description, schema version, creation timestamp, and notes. Supported role
kinds are human operator, risk reviewer, compliance reviewer, research
reviewer, and admin placeholder.

## Safety Boundary

Reviewer role placeholders are not authenticated reviewers. They are not
active user accounts and are not bound to user identity. They cannot approve,
override, recommend, generate DecisionObjects, execute, assign tasks, send
notifications, or bypass safety controls.

Role placeholders do not introduce authentication, identity management,
permission grants, approval workflow execution, override workflow execution,
broker behavior, or execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
