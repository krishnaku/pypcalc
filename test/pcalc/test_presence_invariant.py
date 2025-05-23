# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


import numpy as np
import pytest

from pcalc import Timescale, Presence, PresenceMatrix, PresenceInvariant, Entity, Entity


dummy = Entity()


def make_presences():
    """
    Matrix Time Scale: [0.0, 6.0)

    We have 4 presences:
    - Presence 1: [0.0, 2.0)
    - Presence 2: [1.5, 3.0)
    - Presence 3: [3.0, 4.5)
    - Presence 4: [4.6, ∞)  (open-ended)

    """
    return [
        Presence(boundary=dummy, element=Entity(), start=0.0, end=2.0),
        Presence(boundary=dummy, element=Entity(), start=1.5, end=3.0),
        Presence(boundary=dummy, element=Entity(), start=3.0, end=4.5),
        Presence(boundary=dummy, element=Entity(), start=4.6, end=np.inf),
    ]


@pytest.mark.parametrize("case, start, end, expected", [
    # We will test flow rate for various start and end times relative to the
    # timescale end points [0, 6.0)
    ("Only first presence in [0.0, 1.0)", 0.0, 1.0, 1.0),
    ("First two presences in [0.0, 2.5)", 0.0, 2.5, 2 / 3),  # bins: 0, 1, 2
    ("Only third presence in [3.0, 4.0)", 3.0, 4.0, 1.0),
    ("Only open-ended presence in [4.6, 5.5)", 4.6, 5.5, 1.0),
    ("Zero-length window [2.0, 2.0)", 2.0, 2.0, 0.0),
    ("All presences in [0.0, 6.0)", 0.0, 6.0, 4 / 6),
    ("Edge overlap only with last bin [5.9, 6.0)", 5.9, 6.0, 1.0),
])
def test_flow_rate(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    actual = metrics.flow_rate(start, end)
    assert abs(actual - expected) < 1e-6, case


@pytest.mark.parametrize("case, start, end, expected", [
    # We will test flow rate for various start and end times outside the
    # timescale end points [0, 6.0)
    ("Interval outside the time scale: [6.0, 10.0)", 6.0, 10.0, 0.0),
    ("No presences active in [10.0, 11.0)", 10.0, 11.0, 0.0),

    ("Interval just before all presences [–2.0, –1.0)", -2.0, -1.0, 0.0),
    ("Interval ending at start of first presence [–1.0, 0.0)", -1.0, 0.0, 0.0),

])
def test_flow_rate_outside_window(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    with pytest.raises(ValueError):
        metrics.flow_rate(start, end)


@pytest.mark.parametrize("case, start, end, expected", [
    ("Only P1 started before 1.0:3.0", 1.0, 3.0, 1),
    ("Only P2 started before 2.0:4.0", 2.0, 4.0, 1),
    ("None started before 4.6:6.0", 4.6, 6.0, 1),
    ("None started before 0.0:2.0", 0.0, 2.0, 0),
])
def test_starting_presence_count_window(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    result = metrics.starting_presence_count(start, end)
    assert result == expected, case


@pytest.mark.parametrize("case, start, end, expected", [
    ("Only P2 end after 1.0:3.0", 1.0, 3.0, 1),
    ("Only P4 ends after 3.0:4.5", 3.0, 4.5, 1),
    ("Only P3 end after 3.0:3.5", 3.0, 3.5, 1),
    ("None end after 5.0", 0.0, 5.0, 1),  # only P4 overlaps and is open-ended
])
def test_ending_presence_count_window(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    result = metrics.ending_presence_count(start, end)
    assert result == expected, case


@pytest.mark.parametrize("method_name, start, end", [
    ("starting_presence_count", -1.0, 2.0),
    ("starting_presence_count", 1.0, 7.0),
    ("starting_presence_count", -1.0, 10.0),
    ("ending_presence_count", -0.5, 3.0),
    ("ending_presence_count", 2.0, 6.5),
])
def test_starting_ending_counts_out_of_bounds(method_name, start, end):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    method = getattr(metrics, method_name)

    with pytest.raises(ValueError, match="Presence metrics are not defined outside the time scale"):
        method(start, end)


@pytest.mark.parametrize("case, start, end, expected", [
    ("No arrivals", 5.0, 6.0, 0),
    ("One arrival", 4.0, 5.0, 1),
    ("Two arrivals", 3.0, 5.0, 2),
    ("Three arrivals", 0.0, 4.0, 3),
    ("All arrivals", 0.0, 6.0, 4),
])
def test_arrival_count(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    assert metrics.arrival_count(start, end) == expected, case


@pytest.mark.parametrize("case, start, end, expected", [
    ("No departures", 0.0, 1.0, 0),
    ("One departure", 1.0, 2.5, 1),
    ("Two departures", 2.5, 5.0, 2),
    ("Three departures", 0, 5.0, 3),
    ("All departures", 0.0, 6.0, 3),  # Open-ended presence doesn't count
])
def test_departure_count(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    assert metrics.departure_count(start, end) == expected, case


@pytest.mark.parametrize("case, start, end", [
    ("Mid range window", 1.0, 5.0),
    ("Full timescale window", 0.0, 6.0),
    ("Early subwindow", 0.0, 2.5),
    ("Late subwindow", 3.0, 6.0),
])
def test_flow_rate_consistency(case, start, end):
    presences = make_presences()
    ts = Timescale(0.0, 6.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)

    flow_rate = metrics.flow_rate(start, end)
    start_bin, end_bin = ts.bin_slice(start, end)
    num_bins = end_bin - start_bin

    N = flow_rate * num_bins

    start_count = metrics.starting_presence_count(start, end)
    arrival_count = metrics.arrival_count(start, end)
    lhs = start_count + arrival_count

    departure_count = metrics.departure_count(start, end)
    end_count = metrics.ending_presence_count(start, end)
    rhs = departure_count + end_count

    assert abs(lhs - N) < 1e-6, f"{case}: lhs != flow_rate*T: {lhs} vs {N}"
    assert abs(rhs - N) < 1e-6, f"{case}: rhs != flow_rate*T: {rhs} vs {N}"


def make_variable_binwidth_presences():
    return [
        Presence(boundary=dummy, element=Entity(), start=0.0, end=2.5),
        Presence(boundary=dummy, element=Entity(), start=3.0, end=6.0),
        Presence(boundary=dummy, element=Entity(), start=7.5, end=9.0),
    ]


@pytest.mark.parametrize("case, start, end, expected", [
    ("Single bin window at [0.0, 3.0)", 0.0, 3.0, 1.0),  # Only P1 overlaps bin 0
    ("Window [0.0, 6.0)", 0.0, 6.0, 1.0),  # P1 and P2 over bins 0, 1
    ("Window [6.0, 9.0)", 6.0, 9.0, 1.0),  # Only P3 overlaps bin 2
    ("Window [3.0, 9.0)", 3.0, 9.0, 1.0),  # P2 and P3 over bins 1, 2
    ("Window [0.0, 9.0)", 0.0, 9.0, 1.0),  # All over 3 bins → 3 / 3
    ("Empty window [4.0, 4.0)", 4.0, 4.0, 0.0),  # Zero-width interval → 0
])
def test_flow_rate_variable_bin_width(case, start, end, expected):
    presences = make_variable_binwidth_presences()
    ts = Timescale(t0=0.0, t1=9.0, bin_width=3.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    actual = metrics.flow_rate(start, end)
    assert abs(actual - expected) < 1e-6, f"{case}: {actual} != {expected}"


def make_large_bin_width_presences():
    return [
        Presence(boundary=dummy, element=Entity(), start=0.0, end=2.5),  # bin 0
        Presence(boundary=dummy, element=Entity(), start=3.0, end=6.0),  # bin 1
        Presence(boundary=dummy, element=Entity(), start=7.5, end=9.0),  # bin 2
    ]


@pytest.mark.parametrize("case, start, end", [
    ("Window [0.0, 3.0)", 0.0, 3.0),
    ("Window [3.0, 6.0)", 3.0, 6.0),
    ("Window [6.0, 9.0)", 6.0, 9.0),
    ("Full window [0.0, 9.0)", 0.0, 9.0),
    ("Offset window [1.5, 7.5)", 1.5, 7.5),
])
def test_flow_rate_consistency_with_bin_width(case, start, end):
    presences = make_large_bin_width_presences()
    ts = Timescale(0.0, 9.0, bin_width=3.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)

    flow_rate = metrics.flow_rate(start, end)
    start_bin, end_bin = ts.bin_slice(start, end)
    num_bins = end_bin - start_bin
    N = flow_rate * num_bins

    start_count = sum(
        1 for pm in matrix.presence_map
        if pm.is_active(start_bin, end_bin)
        and pm.start_bin < start_bin
    )

    arrival_count = sum(
        1 for pm in matrix.presence_map
        if pm.is_active(start_bin, end_bin)
        and start_bin <= pm.start_bin < end_bin
    )

    departure_count = sum(
        1 for pm in matrix.presence_map
        if pm.is_active(start_bin, end_bin)
        and not np.isinf(pm.presence.reset_time)
        and start_bin <= ts.bin_index(pm.presence.reset_time) < end_bin
    )

    end_count = sum(
        1 for pm in matrix.presence_map
        if pm.is_active(start_bin, end_bin)
        and (np.isinf(pm.presence.reset_time) or ts.bin_index(pm.presence.reset_time) >= end_bin)
    )

    lhs = start_count + arrival_count
    rhs = departure_count + end_count

    assert abs(lhs - N) < 1e-6, f"{case}: lhs ({lhs}) != flow*N ({N})"
    assert abs(rhs - N) < 1e-6, f"{case}: rhs ({rhs}) != flow*N ({N})"


# Average Residence time tests.
@pytest.mark.parametrize("case, start, end, expected", [
    ("Only P1 fully in window", 0.0, 2.0, (2.0 + 0.5) / 2),
    ("P1 and P2 partial overlap", 1.5, 2.5, (0.5 + 1.0) / 2),
    ("Midrange with P2 and P3", 2.0, 4.0, (1.0 + 1.0) / 2),
    ("Only P4 open-ended clipped to 1.0", 5.0, 6.0, 1.0),
    ("All overlapping presences", 0.0, 6.0, (2.0 + 1.5 + 1.5 + 1.4) / 4),
])
def test_avg_residence_time_per_presence(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    matrix.init_presence_map(presences)
    metrics = PresenceInvariant(matrix)

    actual = metrics.avg_residence_time(start, end)
    assert abs(actual - expected) < 1e-6, f"{case}: got {actual}, expected {expected}"


def test_avg_residence_time_matches_direct_average():
    """This test is reqyied because residence time for presences is defined in
    continuous time, while the avg_residence_time for Presence Matrices is computed
    in bins. We want to make sure that the two definitions always give the same answer
    modulo floating point arithmetic.
    """
    presences = make_presences()
    start, end = 1.0, 5.0

    direct_avg = sum(
        p.residence_time(start, end)
        for p in presences
        if p.residence_time(start, end) > 0
    ) / len([p for p in presences if p.residence_time(start, end) > 0])

    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)

    computed_avg = metrics.avg_residence_time(start, end)

    assert abs(computed_avg - direct_avg) < 1e-6, f"Expected {direct_avg}, got {computed_avg}"


# Test wide bins
def make_wide_bin_presences():
    return [
        Presence(boundary=dummy, element=Entity(), start=1.0, end=5.0),  # spans bins 0–2
        Presence(boundary=dummy, element=Entity(), start=6.0, end=8.0),  # bin 3
    ]


@pytest.mark.parametrize("case, start, end, expected", [
    ("P1 spans [1,5) within [0,6)", 0.0, 6.0, (4.0 + 0.0) / 1),  # Only P1 active, full coverage = 4.0
    ("P2 alone in bin [6,8)", 6.0, 8.0, 2.0),  # Only P2 active, full coverage = 2.0
    ("P1 clipped in [2,4)", 2.0, 4.0, 2.0),  # P1 partially spans one bin
    ("P1 and P2 together in [1,8)", 1.0, 8.0, (4.0 + 2.0) / 2),  # Average over both
    ("Empty window [9,10)", 9.0, 10.0, 0.0),  # No presences
])
def test_avg_residence_time_with_wide_bins(case, start, end, expected):
    presences = make_wide_bin_presences()
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    matrix.init_presence_map(presences)
    metrics = PresenceInvariant(matrix)

    actual = metrics.avg_residence_time(start, end)
    assert abs(actual - expected) < 1e-6, f"{case}: got {actual}, expected {expected}"


def test_avg_residence_time_matches_direct_average_wide_bin():
    """This test is required because residence time for presences is defined in
    continuous time, while the avg_residence_time for Presence Matrices is computed
    in bins. We want to make sure that the two definitions always give the same answer
    modulo floating point arithmetic.
    """
    presences = make_wide_bin_presences()
    start, end = 3.0, 7.0

    direct_avg = sum(
        p.residence_time(start, end)
        for p in presences
        if p.residence_time(start, end) > 0
    ) / len([p for p in presences if p.residence_time(start, end) > 0])

    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)

    computed_avg = metrics.avg_residence_time(start, end)

    assert abs(computed_avg - direct_avg) < 1e-6, f"Expected {direct_avg}, got {computed_avg}"


@pytest.mark.parametrize("case, start, end, expected", [
    ("P1 over [0,2) → 2.0 / 2 bins", 0.0, 2.0, 1.25),
    ("P1 and P2 over [1.5,3.0) → (0.5 + 1.0)/2 bins", 1.5, 3.0, 1.0),
    ("Open ended presence with partial overlap", 5.5, 6.0, 0.5),
])
def test_avg_presence_per_time_bin(case, start, end, expected):
    presences = make_presences()
    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    metrics = PresenceInvariant(matrix)
    result = metrics.avg_presence_per_unit_time(start, end)
    assert abs(result - expected) < 1e-6, f"{case}: got {result}, expected {expected}"


# Presence Invariant consistency tests.

@pytest.mark.parametrize("case, start, end", [
    ("Full interval", 0.0, 6.0),
    ("Early window", 0.0, 2.0),
    ("Mid window", 1.5, 3.5),
    ("Late window", 4.0, 6.0),
    ("Open-ended presence window", 4.6, 6.0),
])
def test_presence_invariant(case, start, end):
    presences = make_presences()
    ts = Timescale(t0=0.0, t1=6.0, bin_width=1.0)
    matrix = PresenceMatrix(presences=presences, time_scale=ts)
    matrix.init_presence_map(presences)
    metrics = PresenceInvariant(matrix)

    # Compute components

    L, Λ, W = metrics.get_presence_metrics(start, end)
    assert L == pytest.approx(Λ * W, rel=1e-6)  # modulo floating point math.
