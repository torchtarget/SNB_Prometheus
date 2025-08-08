"""Fetching and parsing SNB data feeds."""

from __future__ import annotations

import csv
from typing import Dict, Optional, Tuple

import requests


def fetch_csv(cube: str, language: str = "en", params: Optional[Dict[str, str]] = None) -> str:
    """Download CSV content for a cube from the SNB API.

    Parameters mirror the logic of the reference R functions where the URL is
    constructed from the cube identifier and language while additional request
    parameters are appended as query arguments.
    """
    base_url = f"https://data.snb.ch/api/cube/{cube}/data/csv/{language}"
    resp = requests.get(base_url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_latest(csv_text: str) -> Tuple[str, float]:
    """Return (date, value) for the last row in an SNB CSV text.

    SNB downloads include a metadata header separated from the data by a blank
    line and use semicolons as field delimiters. This mirrors the logic found
    in `ReferenceFunctions.R` where the file is read line-wise until the first
    empty line and then parsed as a table.
    """
    lines = csv_text.splitlines()
    try:
        empty_idx = next(i for i, line in enumerate(lines) if not line.strip())
        data_lines = lines[empty_idx + 1 :]
    except StopIteration:
        data_lines = lines

    reader = csv.DictReader(data_lines, delimiter=";")
    rows = list(reader)
    if not rows:
        raise ValueError("CSV contains no data rows")
    last_row = rows[-1]
    date = last_row.get("Date") or last_row.get("DATE")
    value_str = last_row.get("Value") or last_row.get("VALUE")
    if date is None or value_str is None:
        raise ValueError("Expected Date and Value columns")
    value = float(value_str)
    return date, value


def fetch_latest(cube: str, keyseries: str, language: str = "en") -> Tuple[str, float]:
    """Convenience wrapper returning the latest observation for a cube.

    This follows the behaviour of the R `fetch_data` function by building the
    URL from the cube identifier and passing the key series as a filter.
    """
    csv_text = fetch_csv(cube, language, params={"filter[KEYSERIES]": keyseries})
    return parse_latest(csv_text)
