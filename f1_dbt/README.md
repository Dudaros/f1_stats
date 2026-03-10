# F1 Stats Pipeline

A personal data engineering project built to learn and demonstrate 
a modern ELT stack using real Formula 1 data.

## Stack
- **Ingestion**: Python + requests → PostgreSQL
- **Source**: Jolpica API (Ergast-compatible F1 data)
- **Transformation**: dbt (staging + marts)
- **Visualization**: Metabase (coming)
- **Scheduling**: cron (coming)

## Data
Historical F1 data from 2000–2026 covering drivers, races and results 
including sprint sessions.

## Progress
- [x] Ingestion pipeline
- [x] Staging models
- [ ] Marts (fct_results)
- [ ] Metabase dashboards
- [ ] Scheduled runs for 2026 season
