import pandas as pd


def add_time_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    enriched["date"] = pd.to_datetime(enriched["date"])
    enriched = enriched.sort_values(["link_id", "date"])

    grouped = enriched.groupby("link_id", group_keys=False)
    enriched["lag_1"] = grouped["utilization_pct"].shift(1)
    enriched["lag_7"] = grouped["utilization_pct"].shift(7)
    enriched["rolling_mean_7"] = grouped["utilization_pct"].transform(lambda series: series.shift(1).rolling(7).mean())
    enriched["rolling_std_7"] = grouped["utilization_pct"].transform(lambda series: series.shift(1).rolling(7).std()).fillna(0)
    enriched["day_of_week"] = enriched["date"].dt.dayofweek
    enriched["month"] = enriched["date"].dt.month
    enriched["day_index"] = grouped.cumcount()
    return enriched.dropna()


def create_forecast_rows(frame: pd.DataFrame, horizon: int = 14) -> pd.DataFrame:
    future_rows = []
    for link_id, group in frame.groupby("link_id"):
        last_row = group.sort_values("date").iloc[-1]
        future_rows.append(
            {
                "date": pd.to_datetime(last_row["date"]),
                "link_id": link_id,
                "site": last_row["site"],
                "capacity_mbps": last_row["capacity_mbps"],
                "utilization_pct": last_row["utilization_pct"],
            }
        )

    forecast_frame = pd.DataFrame(future_rows)
    forecast_frame["date"] = forecast_frame["date"] + pd.to_timedelta(horizon, unit="D")
    return forecast_frame
