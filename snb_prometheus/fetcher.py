"""Fetching and parsing SNB data feeds."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Tuple

import requests


def fetch_csv(url: str) -> str:
    """Download CSV content from the given URL."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_latest(csv_text: str) -> Tuple[str, float]:
    """Return (date, value) for the last row in the CSV text."""
    reader = csv.reader(StringIO(csv_text))
    header = next(reader, None)
    rows = list(reader)
    if not rows:
        raise ValueError("CSV contains no data rows")
    last_row = rows[-1]
    date = last_row[0]
    value = float(last_row[1])
    return date, value
