# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np
import pytest

from pcalc import Presence, PresenceMap, PresenceMatrix, Timescale
from test.mocks import MockElement, MockBoundary

dummy_boundary = MockBoundary()

presences = [
    Presence(boundary=dummy_boundary, element=MockElement(), start=0.0, end=2.0),
    Presence(boundary=dummy_boundary, element=MockElement(), start=1.5, end=3.5),
    Presence(boundary=dummy_boundary, element=MockElement(), start=2.0, end=4.0),
]

@pytest.mark.parametrize("materialize", [True, False])
def test_matrix_shape(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    assert matrix.shape == (3, 5)

@pytest.mark.parametrize("materialize", [True, False])
def test_matrix_values(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = np.array([
        [1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 1.0, 0.5, 0.0],
        [0.0, 0.0, 1.0, 1.0, 0.0],
    ])
    assert np.allclose(matrix[:], expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_presence_map(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = [PresenceMap(p, ts) for p in presences]
    assert matrix.presence_map == expected

@pytest.mark.parametrize("materialize", [True, False])
def test_matrix_shape_scaled(materialize):
    ts = Timescale(0.0, 10.0, 2.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    assert matrix.shape == (3, 5)

@pytest.mark.parametrize("materialize", [True, False])
def test_matrix_values_scaled(materialize):
    ts = Timescale(0.0, 10.0, 2.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.25, 0.75, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
    ])
    assert np.allclose(matrix[:], expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_presence_map_scaled(materialize):
    ts = Timescale(0.0, 10.0, 2.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = [PresenceMap(p, ts) for p in presences]
    assert matrix.presence_map == expected

@pytest.mark.parametrize("materialize", [True, False])
def test_presence_clipping_at_bounds(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    clipped = [Presence(boundary=dummy_boundary, element=MockElement(), start=-1.0, end=6.0)]
    matrix = PresenceMatrix(clipped, time_scale=ts, materialize=materialize)
    assert np.array_equal(matrix[:], np.array([[1, 1, 1, 1, 1]]))

@pytest.mark.parametrize("materialize", [True, False])
def test_empty_input(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix([], time_scale=ts, materialize=materialize)
    assert matrix.shape == (0, 5)
    assert matrix.presence_map == []

@pytest.mark.parametrize("materialize", [True, False])
def test_partial_overlap_single_bin(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=0.25, end=0.75)
    matrix = PresenceMatrix([p], time_scale=ts, materialize=materialize)
    assert np.allclose(matrix[0, :1], np.array([0.5]))

@pytest.mark.parametrize("materialize", [True, False])
def test_presence_outside_window(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    matrix = PresenceMatrix([p], time_scale=ts, materialize=materialize)
    assert len(matrix.presence_map) == 0
    assert matrix.shape == (0,5)

@pytest.mark.parametrize("materialize", [True, False])
def test_presence_map_outside_window(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=6.0, end=8.0)
    matrix = PresenceMatrix([p], time_scale=ts, materialize=materialize)
    assert matrix.presence_map == []

@pytest.mark.parametrize("materialize", [True, False])
def test_non_integer_scale(materialize):
    ts = Timescale(0.0, 10.0, 2.5)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    assert matrix.shape == (3, 4)

@pytest.mark.parametrize("materialize", [True, False])
def test_fractional_row_sum_consistency(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.25, end=3.75)
    matrix = PresenceMatrix([p], time_scale=ts, materialize=materialize)
    row_sum = matrix[0].sum()
    assert abs(row_sum - (p.end - p.start)) < 1e-6

@pytest.mark.parametrize("materialize", [True, False])
def test_getitem_row_access(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = np.array([1.0, 1.0, 0.0, 0.0, 0.0])
    assert np.allclose(matrix[0], expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_getitem_single_value(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    assert matrix[1, 1] == 0.5
    assert matrix[2, 3] == 1.0

@pytest.mark.parametrize("materialize", [True, False])
def test_getitem_row_slice(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    expected = np.array([0.5, 1.0, 0.5])
    assert np.allclose(matrix[1, 1:4], expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_getitem_invalid_tuple(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    with pytest.raises(ValueError, match="step"):
        _ = matrix[1, 1:4:2]

@pytest.mark.parametrize("materialize", [True, False])
def test_getitem_invalid_index(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)
    with pytest.raises(TypeError, match="Invalid index"):
        _ = matrix["bad"]

@pytest.mark.parametrize("materialize", [True, False])
def test_column_access_single(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)

    col_1 = matrix[:, 1]
    expected = np.array([1.0, 0.5, 0.0])
    assert np.allclose(col_1, expected)

    col_2 = matrix[:, 2]
    expected = np.array([0.0, 1.0, 1.0])
    assert np.allclose(col_2, expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_column_slice_block(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)

    col_block = matrix[:, 1:4]
    expected = np.array([
        [1.0, 0.0, 0.0],
        [0.5, 1.0, 0.5],
        [0.0, 1.0, 1.0],
    ])
    assert np.allclose(col_block, expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_column_slice_with_bounds(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)

    col_block = matrix[:, :2]
    expected = np.array([
        [1.0, 1.0],
        [0.0, 0.5],
        [0.0, 0.0],
    ])
    assert np.allclose(col_block, expected)

@pytest.mark.parametrize("materialize", [True, False])
def test_column_slice_out_of_bounds(materialize):
    ts = Timescale(0.0, 5.0, 1.0)
    matrix = PresenceMatrix(presences, time_scale=ts, materialize=materialize)

    col_block = matrix[:, 4:10]
    expected = np.zeros((3, 1))  # Only bin 4 exists, bin 5–9 ignored
    assert np.allclose(col_block, expected[:, :matrix.shape[1]-4])