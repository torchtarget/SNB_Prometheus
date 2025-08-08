"""HTTP server exposing SNB metrics."""

from __future__ import annotations

import time
from typing import Dict, Tuple

from prometheus_client import start_http_server

from .config import Config, CONFIG
from .fetcher import fetch_latest
from .metrics import set_indicator


def _update_once(indicators: Dict[str, Tuple[str, str]]) -> None:
    for name, (cube, keyseries) in indicators.items():
        _, value = fetch_latest(cube, keyseries)
        set_indicator(name, value)


def run_server(config: Config = CONFIG) -> None:
    start_http_server(config.port)
    while True:
        _update_once(config.indicators)
        time.sleep(config.update_interval)
