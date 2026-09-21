# Day 94: Real-Time Weather Monitoring Dashboard

A CLI monitoring backend that ingests station readings, validates measurements, produces alerts, and returns a live dashboard snapshot. Sample readings keep the lesson reliable without requiring an API key.

## Structure
- `app.py` — monitoring demo
- `stations.py` — station and reading models
- `monitoring.py` — ingestion and dashboard aggregation
- `alerts.py` — weather alert rules

## Run
```bash
cd /Users/arjunvaid/Desktop/sucess_plan/python_mastery_100_days_100_projects/day_94_weather_monitoring_dashboard
python3 app.py
```

Requires Python 3.10+ and no third-party packages.
