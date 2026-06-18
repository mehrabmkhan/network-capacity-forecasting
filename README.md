# Network capacity forecasting

This repo contains a small capacity planning workflow for WAN and enterprise links.

The sample data is synthetic and generated locally so the project stays runnable without private telemetry.

## What is in here

- synthetic link utilization data with seasonal and trend patterns
- a forecasting model that predicts future bandwidth utilization
- congestion risk flags for links that are likely to run hot
- a short business impact summary for planning discussions
- tests, docs, and a notebook walkthrough

## Layout

- `data/` synthetic sample time-series only
- `src/` package code and CLI entry points
- `notebooks/` a walkthrough notebook
- `reports/` example forecast output
- `docs/` project notes and validation steps
- `tests/` unit tests for the core logic
- `diagrams/` architecture sketch
- `screenshots/` placeholder only

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

## Train the model

```bash
python -m network_capacity_forecasting.cli train --data data\synthetic_link_utilization.csv --model artifacts\capacity_model.joblib
```

## Generate the forecast report

```bash
python -m network_capacity_forecasting.cli report --data data\synthetic_link_utilization.csv --model artifacts\capacity_model.joblib --output reports\forecast_summary.md
```

## Validation

```bash
pytest -q
python scripts\validate_sample_data.py
python -m compileall src tests scripts
```

## Cleanup

Remove `artifacts/` and any generated reports if you want a clean tree after a run.
