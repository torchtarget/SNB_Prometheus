import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from snb_prometheus.fetcher import parse_latest

DATA_PATH = pathlib.Path(__file__).parent / "data" / "sample_indicator.csv"


def test_parse_latest() -> None:
    csv_text = DATA_PATH.read_text()
    date, value = parse_latest(csv_text)
    assert date == "2023-02-01"
    assert value == 1.5
