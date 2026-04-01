# OpenSearch to PostgreSQL Data Migration

A minimal, production-ready pipeline that migrates user and activity documents from OpenSearch into PostgreSQL.

This project:
- Creates relational tables for `users`, `address`, and `activity`
- Reads documents from OpenSearch indices (`user`, `activity`)
- Loads data into PostgreSQL with basic idempotency for `users` and `activity`

## Project Structure

- `config/db/connection.py` - OpenSearch and PostgreSQL connection helpers
- `config/db/create_tables.py` - SQL schema creation
- `config/db/models.py` - SQLAlchemy table definitions
- `service/migrate.py` - Data extraction and load logic
- `main.py` - Orchestrates table creation and migration
- `docker-compose.yml` - Local OpenSearch and PostgreSQL services

## Requirements

- Python 3.9+
- OpenSearch and PostgreSQL (local or dockerized)

## Clone and Install

Clone the repository:

```bash
git clone https://github.com/Ali-Haidar-159/opensearch-data-migration.git
cd opensearch-data-migration
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=admin

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=migration_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

## Running Locally

1. Start services (if using Docker):

```bash
docker-compose up -d
```

This starts OpenSearch, OpenSearch Dashboards, and PostgreSQL from `docker-compose.yml`.

2. Run the migration:

```bash
python main.py
```

This will:
- Create tables (if they do not exist)
- Migrate data from OpenSearch to PostgreSQL

## OpenSearch Index Expectations

This project expects two indices:

- `user`
- `activity`

Example documents:

`user` document:

```json
{
  "id": "u1",
  "name": "Alice Johnson",
  "email": "alice.j@example.com",
  "age": 28,
  "address": {
    "street": "123 Maple St",
    "city": "New York",
    "country": "USA"
  }
}
```

`activity` document:

```json
{
  "id": "a9",
  "user_id": "u7",
  "action": "search",
  "location": "Sydney",
  "timestamp": "2026-03-31T10:40:00Z",
  "ip_address": "101.20.30.40"
}
```

## Notes

- IDs are stored as strings in PostgreSQL to match OpenSearch documents.
- The migration uses `ON CONFLICT (id) DO NOTHING` to avoid duplicates for `users` and `activity`.
- The `address` table stores one row per user per activity location found, and does not de-duplicate.
- OpenSearch connections use SSL (`use_ssl=True`) with certificate verification disabled by default in `config/db/connection.py`.
- OpenSearch scroll size is 100 with a 2 minute scroll window (`service/migrate.py`).

## Troubleshooting

- If tables already exist with different column types, drop them or alter them before re-running `create_tables.py`.
- Ensure OpenSearch indices are populated before running the migration.
