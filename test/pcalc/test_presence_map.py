# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


import pytest
import numpy as np


from pcalc import Presence, PresenceMap, Timescale
from .mocks import MockElement, MockBoundary

dummy_boundary = MockBoundary()

def test_full_overlap_single_bin():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.0, end=2.0)
    pm = PresenceMap(p, ts)
    assert pm.is_mapped
    assert pm.start_bin == 1
    assert pm.end_bin == 2
    assert pm.start_value == 1.0
    assert pm.end_value == 0.0

def test_partial_overlap_start_and_end():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=0.25, end=2.75)
    pm = PresenceMap(p, ts)
    assert pm.is_mapped
    assert pm.start_bin == 0
    assert pm.end_bin == 3
    assert np.isclose(pm.start_value, 0.75)
    assert np.isclose(pm.end_value, 0.75)

def test_unmapped_presence():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    pm = PresenceMap(p, ts)
    assert not pm.is_mapped
    assert pm.start_bin == -1
    assert pm.end_bin == -1
    assert pm.start_value == -1.0
    assert pm.end_value == -1.0

def test_exact_bin_edges():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=2.0, end=4.0)
    pm = PresenceMap(p, ts)
    assert pm.is_mapped
    assert pm.start_bin == 2
    assert pm.end_bin == 4
    assert pm.start_value == 1.0
    assert pm.end_value == 1.0

def test_same_bin_partial_presence():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.1, end=1.4)
    pm = PresenceMap(p, ts)
    assert pm.is_mapped
    assert pm.start_bin == 1
    assert pm.end_bin == 2
    assert np.isclose(pm.start_value, 0.3)
    assert pm.end_value == 0.0

# Presence Value Test

@pytest.fixture
def simple_timescale():
    # 10 bins from t=0.0 to t=10.0, width = 1.0
    return Timescale(t0=0.0, t1=10.0, bin_width=1.0)

def test_full_overlap_returns_correct_value(simple_timescale):
    presence = Presence(start=2.0, end=6.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    value = pm.presence_value_in(2.0, 6.0)
    assert 3.0 < value <= 4.0  # Includes fractional bins

def test_partial_overlap_start(simple_timescale):
    presence = Presence(start=2.0, end=6.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    value = pm.presence_value_in(3.0, 6.0)
    assert value < pm.presence_value  # Clipped start reduces presence
    assert value > 0.0

def test_partial_overlap_end(simple_timescale):
    presence = Presence(start=2.0, end=6.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    value = pm.presence_value_in(2.0, 4.0)
    assert value < pm.presence_value
    assert value > 0.0

def test_no_overlap_returns_zero(simple_timescale):
    presence = Presence(start=2.0, end=4.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    value = pm.presence_value_in(5.0, 6.0)
    assert value == 0.0

def test_exact_bin_match(simple_timescale):
    presence = Presence(start=3.0, end=4.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    value = pm.presence_value_in(3.0, 4.0)
    assert 0.9 <= value <= 1.0  # Allow tolerance for partial bin

def test_identity_of_presence_value_property(simple_timescale):
    presence = Presence(start=1.5, end=5.5, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, simple_timescale)

    assert abs(pm.presence_value - pm.presence_value_in(0.0, 10.0)) < 1e-6


def test_exact_fit_with_wide_bin():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    presence = Presence(start=2.0, end=4.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, ts)

    value = pm.presence_value_in(2.0, 4.0)
    assert value == 2.0

def test_partial_overlap_with_wide_bin():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    presence = Presence(start=3.0, end=4.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, ts)

    value = pm.presence_value_in(2.0, 4.0)
    assert value == 1.0  # Half of [2–4)

def test_multi_bin_presence_with_wide_bins():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    presence = Presence(start=1.0, end=7.0, element=MockElement(), boundary=dummy_boundary)
    pm = PresenceMap(presence, ts)

    value = pm.presence_value_in(0.0, 10.0)
    assert pytest.approx(value, 0.01) == 6.0
