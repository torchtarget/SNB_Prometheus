"""CLI entry point for SNB Prometheus service."""

from __future__ import annotations

import argparse

from .backfill import backfill
from .server import run_server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Fetch historical data and load it into Prometheus before starting the server",
    )
    args = parser.parse_args()

    if args.backfill:
        backfill()
    run_server()


if __name__ == "__main__":
    main()
