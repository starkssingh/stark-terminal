# Provider No External Calls Audit

Prompt 25 audits provider external-call boundaries after Prompts 20-24.

## No External Call Posture

Provider modules are local/governance only. They must not call NSE, BSE, brokers, vendors, web pages, cloud services, or external validation systems.

Current provider layers:

- Provider Guardrails: governance contracts only.
- Provider Readiness and Candidate Selection: metadata, risk scoring, and capability gap analysis only.
- Local Sample Provider: synthetic/local/test-only generated responses.
- Local File Provider: explicit local test/dev files under path safety checks.

## Import And Dependency Boundary

Provider modules and provider API routes must not import or use external-call libraries such as `requests`, `httpx`, `aiohttp`, socket clients, URL openers, or provider SDKs. No scraping dependencies, provider SDKs, or broker/trading SDKs are allowed.

The project may keep FastAPI/TestClient support dependencies for tests, but provider implementation modules must remain free of external-call clients.

## File And API Boundary

Local File Provider rejects network paths such as HTTP, S3, GS, FTP, UNC, and `file://`. It also rejects path traversal, symlink escape where practical, unsupported extensions, missing files, directories, and secret-like path text.

Provider API endpoints remain contract, health, template, and tiny sample surfaces only. They do not accept arbitrary file paths, do not read caller-supplied files, do not expose secrets, do not approve providers, and do not return live data.

## Test Posture

Tests are deterministic and local. They use synthetic fixtures, local sample instruments, temporary local files, and static import/dependency checks. They require no external services, no provider credentials, no SDKs, no scraping, and no network.

## Audit Verdict

Provider external-call posture passes the Prompt 25 audit if verification passes:

- no external calls.
- no external provider calls.
- no scraping.
- no network-path file reads.
- no provider SDKs.
- no broker/trading SDKs.
- no credentials.
- no real market ingestion.
- no production approval.
- no execution APIs.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
