from pathlib import Path

import pandas as pd

from .features import add_time_features
from .model import FEATURE_COLUMNS


def forecast_links(frame: pd.DataFrame, model_payload: dict) -> pd.DataFrame:
    model = model_payload["model"]
    engineered = add_time_features(frame)
    latest_rows = engineered.sort_values("date").groupby("link_id").tail(1)
    forecast_input = latest_rows[FEATURE_COLUMNS]
    forecast_output = latest_rows[["date", "link_id", "site", "capacity_mbps", "utilization_pct"]].copy()
    forecast_output["forecast_utilization_pct"] = model.predict(forecast_input)
    forecast_output["congestion_risk"] = forecast_output["forecast_utilization_pct"].apply(
        lambda value: "high" if value >= 85 else "medium" if value >= 70 else "low"
    )
    forecast_output["upgrade_note"] = forecast_output["forecast_utilization_pct"].apply(
        lambda value: "review upgrade window" if value >= 75 else "monitor"
    )
    risk_order = {"high": 3, "medium": 2, "low": 1}
    forecast_output["risk_score"] = forecast_output["congestion_risk"].map(risk_order)
    forecast_output = forecast_output.sort_values(["risk_score", "forecast_utilization_pct"], ascending=[False, False])
    return forecast_output.drop(columns=["risk_score"])


def build_report(forecast: pd.DataFrame, metrics: dict) -> str:
    counts = forecast["congestion_risk"].value_counts().reindex(["high", "medium", "low"], fill_value=0)
    lines = [
        "# Network capacity forecast summary",
        "",
        "This summary is based on synthetic utilization data only.",
        "",
        f"- MAE: {metrics['mae']:.2f}",
        f"- RMSE: {metrics['rmse']:.2f}",
        f"- MAPE: {metrics['mape']:.2f}%",
        f"- High risk links: {int(counts['high'])}",
        f"- Medium risk links: {int(counts['medium'])}",
        f"- Low risk links: {int(counts['low'])}",
        "",
        "## Forecast rows",
        "",
    ]

    for _, row in forecast.iterrows():
        lines.append(
            f"- {row['link_id']} | {row['site']} | current={row['utilization_pct']:.1f}% | forecast={row['forecast_utilization_pct']:.1f}% | risk={row['congestion_risk']} | {row['upgrade_note']}"
        )

    lines.extend(
        [
            "",
            "## Business impact",
            "",
            "- Keep the highest-risk links on the capacity review list first.",
            "- Use the forecast to pre-book maintenance windows before utilization crosses the warning threshold.",
            "- Treat the synthetic data as a planning exercise, not as evidence of production performance.",
        ]
    )

    return "\n".join(lines)


def write_report(path: str | Path, report: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(report, encoding="utf-8")
