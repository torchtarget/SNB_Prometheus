"""Prometheus metric helpers."""

from prometheus_client import Gauge

indicator_gauge = Gauge(
    "snb_indicator_value",
    "Latest value for SNB macroeconomic indicators",
    labelnames=["indicator"],
)


def set_indicator(indicator: str, value: float) -> None:
    """Set the gauge for the given indicator."""
    indicator_gauge.labels(indicator=indicator).set(value)
