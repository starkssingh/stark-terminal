# Migrations

Alembic migration files live in `alembic/versions/`.

Prompt 02 creates the migration foundation for PostgreSQL-ready metadata tables while keeping SQLite available for local tests/dev fallback. `DATABASE_URL` is read from environment/configuration and must never be committed with secrets.

Useful commands after installing dependencies:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

Do not add TimescaleDB hypertables, market-data ingestion tables, broker execution tables, or credential tables in Prompt 02.
