# Research Artifact Registry API No Paper Parsing Policy

Prompt 71 does not ingest papers, parse papers, parse PDFs, ingest arXiv
records, run LLM paper analysis, extract methods, extract strategies, generate
code from papers, generate backtests from papers, or create paper-to-strategy
paths.

Paper artifacts remain metadata/reference placeholders only. API responses do
not return parsed paper content, method extraction, strategy extraction,
strategy code, backtest parameters, backtest results, recommendations,
confidence scores, DecisionObjects, readiness-to-trade, broker controls, or
execution controls.

The API contract skeleton remains read-only and unavailable-by-default.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
