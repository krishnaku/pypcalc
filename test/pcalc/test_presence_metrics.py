# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

import pytest
import numpy as np

from metamodel import Presence
from pcalc import Timescale
from pcalc.presence_matrix import PresenceMatrix
from pcalc.presence_metrics import PresenceMetrics
from test.mocks import MockElement, MockBoundary

dummy = MockBoundary()


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
        Presence(boundary=dummy, element=MockElement(), start=0.0, end=2.0),
        Presence(boundary=dummy, element=MockElement(), start=1.5, end=3.0),
        Presence(boundary=dummy, element=MockElement(), start=3.0, end=4.5),
        Presence(boundary=dummy, element=MockElement(), start=4.6, end=np.inf),
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)
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
    metrics = PresenceMetrics(matrix)

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