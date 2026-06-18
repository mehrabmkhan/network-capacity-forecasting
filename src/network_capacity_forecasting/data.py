from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "date",
    "link_id",
    "site",
    "capacity_mbps",
    "utilization_mbps",
    "utilization_pct",
    "ticket_count",
    "outage_count",
]


def load_utilization_data(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = [column for column in EXPECTED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing utilization columns: {', '.join(missing)}")
    return frame[EXPECTED_COLUMNS].copy()
