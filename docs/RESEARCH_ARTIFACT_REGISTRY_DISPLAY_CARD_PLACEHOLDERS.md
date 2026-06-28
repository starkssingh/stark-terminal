# Research Artifact Registry Display Card Placeholders

Prompt 72 creates backend artifact card placeholder contracts for future Research Artifact Registry display surfaces.

Card placeholders may contain titles, placeholder artifact kinds, lifecycle status placeholders, tags, and safety notes. They do not render a card in a frontend or desktop shell.

Card placeholders must never include:

- active UI state
- frontend component code
- desktop widget definitions
- file content previews
- parsed paper content
- generated strategy content
- backtest metrics
- recommendation, action, confidence, DecisionObject, readiness-to-trade, broker control, or execution fields

The display card contract is backend-only, read-only, unavailable-by-default, and safe for the current Mac mini M2 development environment and future Windows-native desktop target because it does not assume a platform UI.
