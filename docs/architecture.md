# Architecture

The workflow is built around four steps.

1. Generate synthetic daily utilization for a small set of links.
2. Build lag and rolling-window features from the time series.
3. Train a regressor to forecast next-day utilization.
4. Turn the forecast into congestion flags and upgrade notes.

The synthetic data includes trend and weekly seasonality so the forecast has something meaningful to learn from. It is still only lab data, not production telemetry.

## Design boundaries

The model is a portfolio-scale forecasting workflow, not a production capacity planning system. It does not consume private telemetry, tune models against real carrier traffic, or make procurement claims. The value is in showing the planning pipeline: clean data, engineered features, forecast output, and an operator-readable summary.
