# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import numpy as np
from metamodel import Presence
from pcalc import PresenceMatrix, Timescale
from test.mocks import MockElement, MockBoundary
from pcalc.presence_map import PresenceMap

# Common test data
dummy_boundary = MockBoundary()

presences = [
    Presence(boundary=dummy_boundary, element=MockElement(), start=0.0, end=2.0),
    Presence(boundary=dummy_boundary, element=MockElement(), start=1.5, end=3.5),
    Presence(boundary=dummy_boundary, element=MockElement(), start=2.0, end=4.0),
]

def test_matrix_shape():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.shape == (3, 5)

def test_matrix_values():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    expected = np.array([
        [1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 1.0, 0.5, 0.0],
        [0.0, 0.0, 1.0, 1.0, 0.0],
    ], dtype=float)
    assert np.allclose(matrix.presence_matrix, expected)

def test_presence_map():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    expected_map = [
        PresenceMap(presence, ts)
        for presence in presences
    ]
    assert matrix.presence_map == expected_map

def test_matrix_shape_scaled():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.shape == (3, 5)

def test_matrix_values_scaled():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    expected = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.25, 0.75, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
    ], dtype=float)
    assert np.allclose(matrix.presence_matrix, expected)

def test_presence_map_scaled():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    matrix = PresenceMatrix(presences, time_scale=ts)
    expected_map = [
        PresenceMap(presence, ts)
        for presence in presences
    ]
    assert matrix.presence_map == expected_map

def test_presence_clipping_at_bounds():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    clipped = [Presence(boundary=dummy_boundary, element=MockElement(), start=-1.0, end=6.0)]
    matrix = PresenceMatrix(clipped, time_scale=ts)
    expected = np.array([[1, 1, 1, 1, 1]], dtype=int)
    assert np.array_equal(matrix.presence_matrix, expected)

def test_empty_input():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    matrix = PresenceMatrix([], time_scale=ts)
    assert matrix.presence_matrix.shape == (0, 5)
    assert matrix.presence_map == []

def test_partial_overlap_single_bin():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=0.25, end=0.75)
    matrix = PresenceMatrix([p], time_scale=ts)
    expected = np.array([[0.5]])
    assert np.allclose(matrix.presence_matrix[:, :1], expected)

def test_presence_outside_window():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    matrix = PresenceMatrix([p], time_scale=ts)
    expected = np.zeros((1, 5))
    assert np.allclose(matrix.presence_matrix, expected)

def test_presence_map_outside_window():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    matrix = PresenceMatrix([p], time_scale=ts)
    expected_map = [PresenceMap(p,ts)]
    assert matrix.presence_map == expected_map

def test_non_integer_scale():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.5)
    matrix = PresenceMatrix(presences, time_scale=ts)
    assert matrix.presence_matrix.shape == (3, 4)

def test_fractional_row_sum_consistency():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.25, end=3.75)
    matrix = PresenceMatrix([p], time_scale=ts)
    row_sum = matrix.presence_matrix[0].sum()
    expected_duration = p.end - p.start
    assert abs(row_sum - expected_duration) < 1e-6
