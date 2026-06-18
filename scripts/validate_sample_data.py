from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = {
    "date",
    "link_id",
    "site",
    "capacity_mbps",
    "utilization_mbps",
    "utilization_pct",
    "ticket_count",
    "outage_count",
}


def main() -> int:
    data_path = Path("data") / "synthetic_link_utilization.csv"
    frame = pd.read_csv(data_path)
    missing = EXPECTED_COLUMNS.difference(frame.columns)

    if missing:
        print(f"Missing columns: {sorted(missing)}")
        return 1

    print(f"Loaded {len(frame)} synthetic utilization rows from {data_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
