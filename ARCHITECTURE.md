# SNB Prometheus Architecture

This service retrieves selected macroeconomic indicators published by the Swiss National Bank (SNB) and exposes them as Prometheus metrics.

## Components

- **config** – Defines runtime configuration such as update interval, listening port and indicator source URLs.
- **fetcher** – Downloads SNB CSV feeds and parses the latest available value for each indicator.
- **metrics** – Defines Prometheus gauges and helper functions to update them.
- **server** – Periodically refreshes metrics and exposes a `/metrics` HTTP endpoint for Prometheus to scrape.
- **main** – Entry point that loads configuration and starts the server.
- **backfill** *(future work)* – A module intended to push historical values to Prometheus once using `promtool`.

Each indicator is represented by a Prometheus gauge labelled by its indicator name. The server wakes up at a configurable interval, fetches the latest values for all configured indicators and updates the gauges.

```text
+-----------+       +---------+       +---------+       +---------+
|  config   +-------> fetcher +-------> metrics +-------> server  |
+-----------+       +---------+       +---------+       +----+----+
                                                              |
                                                              v
                                                      Prometheus /metrics scrape
```

The design keeps components decoupled and small, enabling future extensions like historical backfill or additional indicators with minimal changes.

