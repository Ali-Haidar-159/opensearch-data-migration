# OpenSearch to PostgreSQL Data Migration

A minimal, production-ready pipeline that migrates user and activity documents from OpenSearch into PostgreSQL.

This project:
- Creates relational tables for `users`, `address`, and `activity`
- Reads documents from OpenSearch indices (`user`, `activity`)
- Loads data into PostgreSQL with basic idempotency

## Project Structure

- `connection.py` - OpenSearch and PostgreSQL connection helpers
- `create_tables.py` - SQL schema creation
- `migrate.py` - Data extraction and load logic
- `main.py` - Orchestrates table creation, migration, and verification
- `docker-compose.yml` - Local OpenSearch and PostgreSQL services

## Requirements

- Python 3.9+
- OpenSearch and PostgreSQL (local or dockerized)

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

2. Run the migration:

```bash
python main.py
```

This will:
- Create tables (if they do not exist)
- Migrate data from OpenSearch to PostgreSQL
- Print final row counts

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
- The migration uses `ON CONFLICT (id) DO NOTHING` to avoid duplicates.
- SSL verification is disabled for OpenSearch by default in `connection.py`.

## Troubleshooting

- If tables already exist with different column types, drop them or alter them before re-running `create_tables.py`.
- Ensure OpenSearch indices are populated before running the migration.
