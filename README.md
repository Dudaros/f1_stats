# F1 Stats Pipeline

A data engineering pipeline that ingests Formula 1 historical data (2000–2026) into PostgreSQL using the Jolpica/Ergast API.

## Stack
- Python (requests, psycopg2)
- PostgreSQL
- dbt (coming)
- Metabase (coming)

## Structure
- `ingestion/` - Python scripts to pull data from Jolpica API into PostgreSQL

## Data Model
Three tables:
- `drivers` - all F1 drivers
- `races` - race and sprint sessions per season
- `results` - per-driver results per session

## Setup
1. Create a PostgreSQL database named `f1`
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run `pip install -r requirements.txt`
4. Run `python ingestion/ingest.py`
