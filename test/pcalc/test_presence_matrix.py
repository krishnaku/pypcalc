# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import numpy as np

from metamodel import Presence
from pcalc import PresenceMatrixBoolean, PresenceMatrixReal  # adjust import path
from test.mocks import MockElement, MockBoundary

from pcalc.presence_matrix import PresenceMap

# Common test data
dummy_boundary = MockBoundary()

presences = [
    Presence(boundary=dummy_boundary, element=MockElement(), start=0.0, end=2.0),
    Presence(boundary=dummy_boundary, element=MockElement(), start=1.5, end=3.5),
    Presence(boundary=dummy_boundary, element=MockElement(), start=2.0, end=4.0),
]


def test_boolean_matrix_shape_and_dtype():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.shape == (3, 5)
    assert matrix.presence_matrix.dtype == int


def test_boolean_matrix_values():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([
        [1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
    ], dtype=int)
    assert np.array_equal(matrix.presence_matrix, expected)


def test_boolean_matrix_presence_map():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected_map = [
        PresenceMap(presences[0], 0, 0, 2),
        PresenceMap(presences[1], 1, 1, 3),
        PresenceMap(presences[2], 2, 2, 4),
    ]
    assert matrix.presence_map == expected_map


def test_boolean_matrix_time_bins():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected_bins = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    assert np.allclose(matrix.time_bins, expected_bins)


def test_real_matrix_dtype_and_shape():
    matrix = PresenceMatrixReal(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    assert matrix.presence_matrix is not None
    assert matrix.presence_matrix.dtype == float
    assert matrix.presence_matrix.shape == (3, 5)


def test_real_matrix_values():
    matrix = PresenceMatrixReal(presences, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([
        [1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 1.0, 0.0],
    ], dtype=float)
    assert np.allclose(matrix.presence_matrix, expected)


def test_presence_clipping_at_bounds():
    clipped = [Presence(boundary=dummy_boundary, element=MockElement(), start=-1.0, end=6.0)]
    matrix = PresenceMatrixBoolean(clipped, start_time=0.0, end_time=5.0, time_scale=1.0)
    expected = np.array([[1, 1, 1, 1, 1]], dtype=int)
    assert np.array_equal(matrix.presence_matrix, expected)

def test_boolean_matrix_values_scaled():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    expected = np.array([
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ], dtype=int)
    assert np.array_equal(matrix.presence_matrix, expected)

def test_boolean_matrix_presence_map_scaled():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    expected_map = [
        PresenceMap(presences[0], 0, 0, 1),
        PresenceMap(presences[1], 1, 0, 1),
        PresenceMap(presences[2], 2, 1, 2),
    ]
    assert matrix.presence_map == expected_map

def test_boolean_matrix_time_bins_scaled():
    matrix = PresenceMatrixBoolean(presences, start_time=0.0, end_time=10.0, time_scale=2.0)
    expected_bins = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
    assert np.allclose(matrix.time_bins, expected_bins)

