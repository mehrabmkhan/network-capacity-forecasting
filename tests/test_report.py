from scripts.generate_synthetic_data import build_rows
from network_capacity_forecasting.model import train_forecast_model
from network_capacity_forecasting.report import build_report, forecast_links


def test_report_mentions_synthetic_data_and_business_notes():
    frame = build_rows(days=180)
    metrics = train_forecast_model(frame)
    forecast = forecast_links(frame, {"model": metrics.model})
    report = build_report(forecast, {"mae": metrics.mae, "rmse": metrics.rmse, "mape": metrics.mape})

    assert "synthetic utilization data" in report
    assert "Business impact" in report
