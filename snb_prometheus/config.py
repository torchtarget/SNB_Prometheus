from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Config:
    """Runtime configuration for the service."""

    port: int = 8000
    update_interval: int = 24 * 60 * 60  # seconds
    indicators: Dict[str, str] = field(
        default_factory=lambda: {
            "policy_rate": "https://data.snb.ch/api/cube/monzano/data?filter[KEYSERIES]=A.POLIRATE&download=true"
        }
    )


CONFIG = Config()
