# Validation

Run these commands from the repo root:

```bash
python -m pip install -e . -r requirements.txt
python scripts/generate_synthetic_data.py
python scripts/validate_sample_data.py
pytest -q
python -m network_capacity_forecasting.cli train --data data/synthetic_link_utilization.csv --model artifacts/capacity_model.joblib
python -m network_capacity_forecasting.cli report --data data/synthetic_link_utilization.csv --model artifacts/capacity_model.joblib --output reports/forecast_summary.md
```

The generated report should include forecasted utilization, risk flags, and a short planning note.

CI runs package install, syntax compilation, sample data generation, sample data validation, and pytest for relevant pushes and pull requests. The workflow can also be started manually from GitHub Actions.
