"""CLI entry point for SNB Prometheus service."""

from .server import run_server


if __name__ == "__main__":
    run_server()
