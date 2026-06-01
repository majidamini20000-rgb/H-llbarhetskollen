from __future__ import annotations

import pytest

from app.services.emissions import Factor, calculate_co2e


def test_calculate_co2e_ok():
    factors = {
        ("travel", "car"): Factor(category="travel", key="car", unit="km", co2e_per_unit=0.2),
    }
    assert calculate_co2e("travel", "car", 10, factors) == pytest.approx(2.0)


def test_calculate_co2e_missing_factor():
    factors = {}
    with pytest.raises(KeyError):
        calculate_co2e("travel", "car", 10, factors)


def test_calculate_co2e_invalid_amount():
    factors = {("travel", "car"): Factor(category="travel", key="car", unit="km", co2e_per_unit=0.2)}
    with pytest.raises(ValueError):
        calculate_co2e("travel", "car", 0, factors)