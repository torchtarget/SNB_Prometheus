"""Utilities for importing historical SNB data into Prometheus."""

from __future__ import annotations

import csv
import subprocess
import tempfile
from datetime import datetime
from typing import List, Tuple

from .config import Config, CONFIG
from .fetcher import fetch_csv


# Prometheus metric name used throughout the project
_METRIC_NAME = "snb_indicator_value"


def _parse_series(csv_text: str) -> List[Tuple[int, float]]:
    """Parse a full CSV download into ``(timestamp, value)`` pairs.

    The SNB CSV format contains a metadata header separated from the data by a
    blank line and uses semicolons as field delimiters. Each data row contains a
    ``Date`` column and a ``Value`` column. The returned timestamps are Unix
    epoch seconds suitable for Prometheus.
    """

    lines = csv_text.splitlines()
    try:
        empty_idx = next(i for i, line in enumerate(lines) if not line.strip())
        data_lines = lines[empty_idx + 1 :]
    except StopIteration:
        data_lines = lines

    reader = csv.DictReader(data_lines, delimiter=";")
    series: List[Tuple[int, float]] = []
    for row in reader:
        date = row.get("Date") or row.get("DATE")
        value = row.get("Value") or row.get("VALUE")
        if date is None or value is None:
            continue
        timestamp = int(datetime.fromisoformat(date).timestamp())
        series.append((timestamp, float(value)))
    return series


def _build_openmetrics(config: Config) -> str:
    """Return OpenMetrics text for all indicators in *config*."""

    lines: List[str] = [f"# TYPE {_METRIC_NAME} gauge\n"]
    for indicator, (cube, keyseries) in config.indicators.items():
        csv_text = fetch_csv(cube, params={"filter[KEYSERIES]": keyseries})
        for ts, value in _parse_series(csv_text):
            lines.append(
                f"{_METRIC_NAME}{{indicator=\"{indicator}\"}} {value} {ts}\n"
            )
    return "".join(lines)


def backfill(
    config: Config = CONFIG,
    *,
    promtool_path: str = "promtool",
    tsdb_path: str = ".",
) -> None:
    """Fetch historical data and load it into Prometheus via ``promtool``.

    Parameters
    ----------
    config:
        Configuration describing which indicators to import.
    promtool_path:
        Path to the ``promtool`` binary.
    tsdb_path:
        Destination directory for the created TSDB blocks. This should point to
        Prometheus' data directory.
    """

    metrics_text = _build_openmetrics(config)
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(metrics_text)
        tmp_path = tmp.name

    subprocess.run(
        [
            promtool_path,
            "tsdb",
            "create-blocks-from",
            "openmetrics",
            tmp_path,
            tsdb_path,
        ],
        check=True,
    )
