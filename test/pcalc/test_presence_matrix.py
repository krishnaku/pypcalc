# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import numpy as np

from metamodel import Presence
from pcalc import PresenceMatrix
from test.mocks import MockElement, MockBoundary

from pcalc.presence_matrix import PresenceMap

# Common test data
dummy_boundary = MockBoundary()

presences = [
    Presence(boundary=dummy_boundary, element=MockElement(), start=0.0, end=2.0),
    Presence(boundary=dummy_boundary, element=MockElement(), start=1.5, end=3.5),
    Presence(boundary=dummy_boundary, element=MockElement(), start=2.0, end=4.0),
]


def test_matrix_shape():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.shape == (3, 5)


def test_matrix_values():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([
        [1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 1.0, 0.5, 0.0],
        [0.0, 0.0, 1.0, 1.0, 0.0],
    ], dtype=float)
    assert np.allclose(matrix.presence_matrix, expected)

def test_presence_map():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected_map = [
        PresenceMap(presences[0], 0, 0, 2),
        PresenceMap(presences[1], 1, 1, 4),
        PresenceMap(presences[2], 2, 2, 4),
    ]
    assert matrix.presence_map == expected_map

def test_matrix_shape_scaled():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.shape == (3, 5)


def test_matrix_values_scaled():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    expected = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.25, 0.75, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
    ], dtype=float)
    assert np.allclose(matrix.presence_matrix, expected)

def test_presence_map_scaled():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    expected_map = [
        PresenceMap(presences[0], 0, 0, 1),
        PresenceMap(presences[1], 1, 0, 2),
        PresenceMap(presences[2], 2, 1, 2),
    ]
    assert matrix.presence_map == expected_map


def test_presence_clipping_at_bounds():
    clipped = [Presence(boundary=dummy_boundary, element=MockElement(), start=-1.0, end=6.0)]
    matrix = PresenceMatrix(clipped, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([[1, 1, 1, 1, 1]], dtype=int)
    assert np.array_equal(matrix.presence_matrix, expected)


def test_empty_input():
    matrix = PresenceMatrix([], start_time=0.0, end_time=5.0, time_scale=1.0)
    assert matrix.presence_matrix.shape == (0, 5)
    assert matrix.presence_map == []

def test_partial_overlap_single_bin():
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=0.25, end=0.75)
    matrix = PresenceMatrix([p], start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([[0.5]])
    assert np.allclose(matrix.presence_matrix[:, :1], expected)

def test_presence_outside_window():
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    matrix = PresenceMatrix([p], start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.zeros((1, 5))
    assert np.allclose(matrix.presence_matrix, expected)

def test_non_integer_scale():
    matrix = PresenceMatrix(presences, start_time=0.0, end_time=10.0, time_scale=2.5)
    assert matrix.presence_matrix.shape == (3, 4)

def test_fractional_row_sum_consistency():
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.25, end=3.75)
    matrix = PresenceMatrix([p], start_time=0.0, end_time=5.0, time_scale=1.0)
    row_sum = matrix.presence_matrix[0].sum()
    expected_duration = p.end - p.start
    assert abs(row_sum - expected_duration) < 1e-6
