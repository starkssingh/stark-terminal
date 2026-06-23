# Decision Override Prohibition

Prompt 39 implements override prohibition contracts.

Overrides are prohibited. Emergency bypass is not implemented. Any bypass would require a future prompt, explicit safety policy, audit coverage, and tests before it could be considered.

No manual override can enable:

- recommendations;
- action generation;
- confidence scoring;
- DecisionObject generation;
- execution APIs;
- broker orders;
- market-state decisions.

The override prohibition is part of the Decision Safety blocked output policy. It is guardrails-only and not a production approval mechanism. Mac mini M2 development and Windows-native targeting remain documented constraints.
