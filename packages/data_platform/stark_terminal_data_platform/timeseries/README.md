# Stark Terminal Time-Series Foundation

This package contains TimescaleDB/time-series foundation helpers for Stark Terminal.

Prompt 03 does not ingest data and does not require TimescaleDB locally. The SQL helpers return migration-planning strings for extension and hypertable setup; they do not execute SQL.

Actual deployment needs PostgreSQL with the TimescaleDB extension installed and enabled through explicit configuration.
