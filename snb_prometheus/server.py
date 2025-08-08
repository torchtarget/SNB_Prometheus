"""HTTP server exposing SNB metrics."""

from __future__ import annotations

import time
from typing import Dict

from prometheus_client import start_http_server

from .config import Config, CONFIG
from .fetcher import fetch_csv, parse_latest
from .metrics import set_indicator


def _update_once(indicators: Dict[str, str]) -> None:
    for name, url in indicators.items():
        csv_text = fetch_csv(url)
        _, value = parse_latest(csv_text)
        set_indicator(name, value)


def run_server(config: Config = CONFIG) -> None:
    start_http_server(config.port)
    while True:
        _update_once(config.indicators)
        time.sleep(config.update_interval)
