# Decision Review Queue Placeholders

Prompt 45 defines review queue placeholders for future Decision Desk human
review workflow planning.

## Schema

Each queue placeholder has a queue id, queue kind, name, description, schema
version, creation timestamp, and notes. Supported queue kinds are placeholder
queue, evidence queue, safety queue, validation queue, and blocked queue.

## Safety Boundary

Review queue placeholders are not active queues. They are not persisted. They
do not assign tasks, send notifications, grant approval, grant override, expose
execution, or become a bypass path. A queue placeholder is not an approval
route and is not readiness-to-trade.

Queue placeholders remain unavailable-by-default planning artifacts with no
active workflow behavior.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
