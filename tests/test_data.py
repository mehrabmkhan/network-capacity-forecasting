from pathlib import Path

from network_capacity_forecasting.data import EXPECTED_COLUMNS, load_utilization_data


def test_load_utilization_data_has_expected_columns(tmp_path: Path):
    data_path = tmp_path / "capacity.csv"
    data_path.write_text(
        ",".join(EXPECTED_COLUMNS) + "\n" + ",".join(["1"] * len(EXPECTED_COLUMNS)),
        encoding="utf-8",
    )

    frame = load_utilization_data(data_path)
    assert list(frame.columns) == EXPECTED_COLUMNS
