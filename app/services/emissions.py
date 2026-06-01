from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Factor:
    category: str
    key: str
    unit: str
    co2e_per_unit: float


FactorMap = Dict[Tuple[str, str], Factor]


def calculate_co2e(category: str, key: str, amount: float, factors: FactorMap) -> float:
    """Beräkna CO₂e för en aktivitet.

    - category: t.ex. 'travel', 'food', 'energy'
    - key: t.ex. 'car', 'train', 'beef'
    - amount: t.ex. km, portioner, kWh (beror på unit)
    - factors: mapping (category, key) -> Factor

    (För kursen: håll beräkningen transparent och enkel.)
    """
    if amount <= 0:
        raise ValueError("amount must be > 0")

    factor = factors.get((category, key))
    if factor is None:
        raise KeyError(f"No emission factor for ({category}, {key})")

    return amount * factor.co2e_per_unit