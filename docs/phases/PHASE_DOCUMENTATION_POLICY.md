# Phase Documentation Policy

Status: documentation/test consolidation interlude.

Future Stark Terminal docs should be phase-first, not prompt-first.

Prompt logs remain the chronological source of what happened, but detailed audits should be grouped by phase or boundary. Audit docs should summarize the phase and its safety constraints instead of splitting every forbidden capability into a separate document unless a separate file is genuinely useful.

Documentation should support development, not dominate it.

Default future prompt expectation:

- one core doc for the feature or phase
- one explicit safety section
- one focused test file per meaningful feature/module
- grouped phase or boundary tests when a new safety surface appears

Detailed one-off audit docs are still allowed for major milestones, new boundary types, or compliance-critical decisions. They should not be the default for ordinary prompt work.

## Archive Pass 2 Note

Archive Pass 2 reinforces this policy by archiving older Strategy Research
Workspace and Research Artifact Registry micro-audit docs where grouped phase
docs and grouped boundary docs already preserve coverage. Phase docs are the
canonical summaries for completed phases; prompt-level micro-audit sprawl
should not be recreated unless a new, material safety boundary requires it.

After the aggressive deletion pass, phase docs plus grouped reports in
`docs/reports/` are canonical for deleted micro-audit details. Prompt-level
micro-audits are superseded unless a specific future feature introduces a new
boundary that cannot be represented cleanly in a phase doc, grouped audit doc,
or grouped report.
