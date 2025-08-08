SNB Prometheus
===============
A lightweight service that fetches selected Swiss National Bank (SNB) macroeconomic indicators (e.g., policy interest rate, CPI YoY, GDP growth) from SNB’s public data portal, parses them, and exposes the latest values as Prometheus-compatible metrics. Supports a one-time historical backfill to Prometheus for full data continuity. Designed for low-frequency, low-volume time series, ideal for home labs with Grafana dashboards.

Definition:

    Inputs: Public SNB CSV data feeds for chosen indicators.

    Outputs: /metrics endpoint exposing Prometheus gauges with standard labels (e.g., country, source).

    Update frequency: Configurable; default 24h scrape interval.

    Retention: Uses Prometheus’ native long-term retention; historical data loaded via promtool once.

    Scope: Macro indicators only; low maintenance, minimal resource usage.

    Integration: Scraped directly by Prometheus, visualised in Grafana, optional alerts on thresholds.

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details. To run the development server:

```bash
pip install -r requirements.txt
python -m snb_prometheus.main
```
