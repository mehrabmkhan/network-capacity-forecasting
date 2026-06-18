from scripts.generate_synthetic_data import build_rows
from network_capacity_forecasting.model import train_forecast_model


def test_training_produces_reasonable_metrics():
    frame = build_rows(days=180)
    result = train_forecast_model(frame)

    assert result.mae < 10
    assert result.rmse < 12
    assert result.mape < 20
