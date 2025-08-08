from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Config:
    """Runtime configuration for the service."""

    port: int = 8000
    update_interval: int = 24 * 60 * 60  # seconds
    indicators: Dict[str, Tuple[str, str]] = field(
        default_factory=lambda: {
            "policy_rate": ("monzano", "A.POLIRATE")
        }
    )


CONFIG = Config()
