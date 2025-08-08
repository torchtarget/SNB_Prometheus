from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Config:
    """Runtime configuration for the service."""

    port: int = 8000
    update_interval: int = 24 * 60 * 60  # seconds
    # Each indicator is defined as a tuple ``(cube, keyseries)`` where ``cube``
    # is the SNB table identifier and ``keyseries`` selects the desired
    # timeseries within that cube.
    indicators: Dict[str, Tuple[str, str]] = field(
        default_factory=lambda: {
            "policy_rate": ("snboffzisa", "LZ"),
        }
    )


CONFIG = Config()

# Configuration covering interest rate and inflation data for Switzerland and
# the United Kingdom using SNB datasets.  This configuration can be passed to
# the server/backfill helpers to expose the additional metrics.
INTEREST_INFLATION_CONFIG = Config(
    indicators={
        "switzerland_interest_rate": ("snboffzisa", "LZ"),
        "uk_interest_rate": ("snboffzisa", "L0"),
        "switzerland_inflation": ("iukpaus", "S"),
        "uk_inflation": ("iukpaus", "VK"),
    }
)
