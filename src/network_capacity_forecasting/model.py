from dataclasses import dataclass
from pathlib import Path
from math import sqrt

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from .features import add_time_features


FEATURE_COLUMNS = ["lag_1", "lag_7", "rolling_mean_7", "rolling_std_7", "day_of_week", "month", "day_index"]


@dataclass
class TrainingResult:
    model: RandomForestRegressor
    mae: float
    rmse: float
    mape: float


def train_forecast_model(frame: pd.DataFrame, random_state: int = 42) -> TrainingResult:
    sorted_frame = frame.copy()
    sorted_frame["date"] = pd.to_datetime(sorted_frame["date"])
    sorted_frame = sorted_frame.sort_values(["link_id", "date"])

    engineered = add_time_features(sorted_frame)
    target = sorted_frame.groupby("link_id", group_keys=False)["utilization_pct"].shift(-1)
    model_frame = engineered.copy()
    model_frame["target_utilization_pct"] = target.loc[engineered.index]
    model_frame = model_frame.dropna(subset=["target_utilization_pct"])
    features = model_frame[FEATURE_COLUMNS]
    target = model_frame["target_utilization_pct"]

    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=250, random_state=random_state)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = sqrt(mean_squared_error(y_test, predictions))
    mape = float((abs((y_test - predictions) / y_test).replace([float("inf")], 0).fillna(0)).mean() * 100)

    return TrainingResult(model=model, mae=mae, rmse=rmse, mape=mape)


def save_model(path: str | Path, result: TrainingResult) -> None:
    payload = {
        "model": result.model,
        "feature_columns": FEATURE_COLUMNS,
        "mae": result.mae,
        "rmse": result.rmse,
        "mape": result.mape,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, path)


def load_model(path: str | Path) -> dict:
    return joblib.load(path)
