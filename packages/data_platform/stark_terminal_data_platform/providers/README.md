# Provider Contracts Package

This package contains read-only market data provider contracts for Stark Terminal.

Prompt 08 does not implement real providers, provider SDKs, scraping, network calls, credentials, broker integrations, or execution APIs. Provider adapters are contract-first and read-only.

Future provider implementations must obey data policy, provider terms, credential handling rules, quality checks, and explicit prompt scope before any ingestion occurs.
