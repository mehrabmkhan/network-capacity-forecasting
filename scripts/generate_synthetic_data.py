from math import sin, pi
from pathlib import Path
from random import Random

import pandas as pd


def build_rows(seed: int = 11, days: int = 365) -> pd.DataFrame:
    rng = Random(seed)
    start_date = pd.Timestamp("2025-01-01")
    links = [
        {"link_id": "wan-01", "site": "metro-core", "capacity_mbps": 1000},
        {"link_id": "wan-02", "site": "enterprise-backup", "capacity_mbps": 500},
        {"link_id": "wan-03", "site": "branch-aggregation", "capacity_mbps": 250},
    ]

    rows: list[dict] = []
    for link in links:
        base = 42 if link["link_id"] == "wan-01" else 35 if link["link_id"] == "wan-02" else 50
        trend = 0.07 if link["link_id"] == "wan-01" else 0.04 if link["link_id"] == "wan-02" else 0.02

        for day in range(days):
            weekly = 8 * sin((day % 7) / 7 * 2 * pi)
            monthly = 5 * sin(day / 30 * 2 * pi)
            noise = rng.gauss(0, 3.5)
            utilization_pct = min(98, max(5, base + day * trend + weekly + monthly + noise))
            utilization_mbps = round(link["capacity_mbps"] * utilization_pct / 100, 1)

            rows.append(
                {
                    "date": (start_date + pd.Timedelta(days=day)).date().isoformat(),
                    "link_id": link["link_id"],
                    "site": link["site"],
                    "capacity_mbps": link["capacity_mbps"],
                    "utilization_mbps": utilization_mbps,
                    "utilization_pct": round(utilization_pct, 1),
                    "ticket_count": max(0, int(rng.gauss(2, 1.5))),
                    "outage_count": 1 if utilization_pct > 90 and rng.random() < 0.15 else 0,
                }
            )

    return pd.DataFrame(rows)


def main() -> int:
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    frame = build_rows()
    frame.to_csv(data_dir / "synthetic_link_utilization.csv", index=False)
    print(f"Wrote {len(frame)} rows to {data_dir / 'synthetic_link_utilization.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
