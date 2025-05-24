# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
import pytest
from datetime import datetime, timedelta
from pcalc  import TimeModel

@pytest.mark.parametrize("unit, expected", [
    ("seconds", 3600.0),
    ("minutes", 60.0),
    ("hours", 1.0),
    ("days", 1.0 / 24),
])
def test_fixed_units_to_float(unit, expected):
    origin = datetime(2025, 1, 1, 0, 0, 0)
    t = origin + timedelta(hours=1)
    tm = TimeModel(origin=origin, unit=unit)
    assert pytest.approx(tm.to_float(t), rel=1e-6) == expected


@pytest.mark.parametrize("unit, value", [
    ("seconds", 90.0),
    ("minutes", 1.5),
    ("hours", 0.25),
    ("days", 2.0),
])
def test_fixed_units_from_float(unit, value):
    origin = datetime(2025, 1, 1, 0, 0, 0)
    tm = TimeModel(origin=origin, unit=unit)
    dt = tm.from_float(value)
    roundtrip = tm.to_float(dt)
    assert pytest.approx(roundtrip, rel=1e-6) == value


def test_months_conversion():
    origin = datetime(2025, 1, 1)
    dt = datetime(2025, 4, 1)
    tm = TimeModel(origin=origin, unit="months")
    assert tm.to_float(dt) == 3.0
    assert tm.from_float(3.0).month == 4


def test_quarters_conversion():
    origin = datetime(2025, 1, 1)
    dt = datetime(2025, 10, 1)
    tm = TimeModel(origin=origin, unit="quarters")
    assert tm.to_float(dt) == 3.0
    assert tm.from_float(2.0).month == 7  # July = start of Q3


def test_years_conversion():
    origin = datetime(2020, 1, 1)
    dt = datetime(2025, 1, 1)
    tm = TimeModel(origin=origin, unit="years")
    assert tm.to_float(dt) == 5.0
    back = tm.from_float(5.0)
    assert back.year == 2025 and back.month == 1 and back.day == 1


def test_partial_months():
    origin = datetime(2025, 1, 1)
    dt = datetime(2025, 2, 15)
    tm = TimeModel(origin=origin, unit="months")
    val = tm.to_float(dt)
    assert 1.4 < val < 1.6  # Approx halfway through Feb
