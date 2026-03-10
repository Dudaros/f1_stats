# F1 Stats Pipeline

A data engineering pipeline built to ingest, transform and visualize 
Formula 1 historical data (2000–2026).

## Stack
- **Ingestion**: Python (requests, psycopg2)
- **Storage**: PostgreSQL
- **Transformation**: dbt
- **Visualization**: Metabase (coming)
- **Scheduling**: cron (coming)

## Structure
- `ingestion/` - pulls data from Jolpica API into PostgreSQL
- `f1_dbt/` - dbt project with staging and marts models

## Data Model
**Raw tables**: `drivers`, `races`, `results`

**Staging**: `stg_drivers`, `stg_races`, `stg_results`

**Marts**: `fct_results` - joined fact table combining drivers, races and results

## Progress
- [x] Ingestion pipeline
- [x] Staging models
- [x] Marts (fct_results)
- [ ] Metabase dashboards
- [ ] Scheduling

## Setup
1. Create a PostgreSQL database named `f1`
2. Run `pip install -r requirements.txt`
3. Run `python ingestion/ingest.py`
4. Run `dbt run` inside `f1_dbt/`# F1 Stats Pipeline

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
