# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np
import pytest

from pcalc import PresenceAssertion, Entity


def test_overlap_true():
    p = PresenceAssertion("x", Entity(), 1.0, 5.0)
    assert p.overlaps(2.0, 4.0) is True
    assert p.overlaps(4.9, 6.0) is True
    assert p.overlaps(0.0, 1.1) is True

def test_overlap_false():
    p = PresenceAssertion("x", Entity(), 1.0, 5.0)
    assert p.overlaps(5.0, 6.0) is False
    assert p.overlaps(0.0, 1.0) is False


def test_duration():
    p = PresenceAssertion("x", Entity(), 1.0, 4.0)
    assert p.mass() == 3.0

def test_duration_inf():
    p = PresenceAssertion("x", Entity(), 1.0, np.inf)
    assert p.mass() == np.inf

def test_residence_time_overlap():
    p = PresenceAssertion("x", Entity(), 1.0, 5.0)
    assert p.mass_contribution(2.0, 6.0) == 3.0

def test_residence_time_no_overlap():
    p = PresenceAssertion("x", Entity(), 1.0, 2.0)
    assert p.mass_contribution(2.0, 3.0) == 0.0

def test_str_representation():
    p = PresenceAssertion("x", Entity("B"), 3.0, 7.0, "observed")
    s = str(p)
    assert "Presence(element=x, boundary=Element[B] name = B (no metadata), interval=[3.0, 7.0), provenance=observed)" in s



@pytest.mark.parametrize("desc, presence_args, window, expected_residence", [
    # Regular case
    ("finite in [0, 1)", (0.0, 1.0), (0.0, 1.0), 1.0),

    # Presence entirely before window
    ("before window", (0.0, 1.0), (1.0, 2.0), 0.0),

    # Presence entirely after window
    ("after window", (2.0, 3.0), (0.0, 2.0), 0.0),

    # Window inside presence
    ("window inside long presence", (0.0, 10.0), (2.0, 4.0), 2.0),

    # Presence with reset_time = inf
    ("open-ended presence clipped by window", (4.6, float("inf")), (4.6, 5.5), 0.9),

    # Presence with onset_time = -inf
    ("started in distant past", (-float("inf"), 1.0), (0.0, 1.0), 1.0),

    # Presence from -inf to inf, full overlap
    ("eternal presence", (-float("inf"), float("inf")), (2.0, 5.0), 3.0),

    # Presence from -inf to finite, partial overlap
    ("infinite start, finite end", (-float("inf"), 3.0), (2.0, 5.0), 1.0),

    # Presence from finite to inf, partial overlap
    ("finite start, infinite end", (3.0, float("inf")), (2.0, 5.0), 2.0),

    # Window with t0 >= t1
    ("zero-length window", (0.0, 1.0), (1.0, 1.0), 0.0),

])
def test_presence_residence_time(desc, presence_args, window, expected_residence):
    p = PresenceAssertion(Entity("e"), Entity("b"), *presence_args)
    t0, t1 = window
    actual = p.mass_contribution(t0, t1)
    assert abs(actual - expected_residence) < 1e-6, f"{desc}: got {actual}, expected {expected_residence}"


@pytest.mark.parametrize("desc, presence_args, window, expected_overlap", [
    # Normal overlap
    ("exact match", (0.0, 1.0), (0.0, 1.0), True),

    # Partial overlap at start
    ("partial overlap start", (0.5, 1.5), (0.0, 1.0), True),

    # Partial overlap at end
    ("partial overlap end", (0.0, 0.5), (0.5, 1.0), False),

    # No overlap - before
    ("no overlap before", (0.0, 0.5), (0.5, 1.0), False),

    # No overlap - after
    ("no overlap after", (1.0, 2.0), (0.0, 1.0), False),

    # Presence inside window
    ("fully inside window", (2.0, 3.0), (1.0, 4.0), True),

    # Window inside presence
    ("window inside presence", (0.0, 10.0), (4.0, 5.0), True),

    # Reset time = inf
    ("infinite reset", (4.6, float("inf")), (4.6, 5.5), True),

    # Onset time = -inf
    ("infinite onset", (-float("inf"), 1.0), (0.0, 1.0), True),

    # Both ends infinite
    ("eternal presence", (-float("inf"), float("inf")), (2.0, 5.0), True),


    # Window with t0 >= t1
    ("zero-length window", (0.0, 1.0), (1.0, 1.0), False),
])
def test_presence_overlaps(desc, presence_args, window, expected_overlap):
    p = PresenceAssertion(Entity("e"), Entity("b"), *presence_args)
    t0, t1 = window
    actual = p.overlaps(t0, t1)
    assert actual == expected_overlap, f"{desc}: got {actual}, expected {expected_overlap}"



@pytest.mark.parametrize("desc, onset, reset, expected_duration", [
    # Standard case
    ("normal duration", 1.0, 3.0, 2.0),

    # Empty presence at t=0
    ("empty presence at origin", 0.0, 0.0, 0.0),

    # Open-ended presence
    ("open-ended presence", 5.0, float("inf"), float("inf")),

    # Reset at infinity, onset before t=0
    ("eternal presence ending never", -float("inf"), float("inf"), float("inf")),

    # Reset finite, onset = -inf → duration = reset - 0
    ("eternal presence ending at t=5", -float("inf"), 5.0, 5.0),

    # Reset finite, onset = -inf → duration = reset - 0
    ("eternal presence ending at t=1", -float("inf"), 1.0, 1.0),

    # Fully finite
    ("short finite presence", 0.5, 1.5, 1.0),
])
def test_presence_duration(desc, onset, reset, expected_duration):
    p = PresenceAssertion(Entity("e"), Entity("b"), onset, reset)
    actual = p.mass()
    if expected_duration == float("inf"):
        assert actual == float("inf"), f"{desc}: got {actual}, expected inf"
    else:
        assert abs(actual - expected_duration) < 1e-6, f"{desc}: got {actual}, expected {expected_duration}"
