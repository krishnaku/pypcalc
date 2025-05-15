# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


import numpy as np
from pcalc import Timescale


def test_num_bins_exact():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.num_bins == 5

def test_num_bins_non_aligned():
    ts = Timescale(0.0, 10.1, 2.0)
    assert ts.num_bins == 6


def test_bin_edges_exact_alignment():
    ts = Timescale(t0=0.0, t1=10.0, bin_width=2.0)
    expected = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
    assert np.allclose(ts.bin_edges(), expected)

def test_bin_edges_partial_bin_ceil():
    ts = Timescale(t0=0.0, t1=9.0, bin_width=2.0)
    expected = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])  # includes extra bin to ceil 9.0
    assert np.allclose(ts.bin_edges(), expected)

def test_bin_edges_nonzero_t0():
    ts = Timescale(t0=1.0, t1=9.0, bin_width=2.0)
    expected = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
    assert np.allclose(ts.bin_edges(), expected)

def test_bin_edges_floating_bin_width():
    ts = Timescale(t0=0.0, t1=1.0, bin_width=0.3)
    edges = ts.bin_edges()
    assert len(edges) == ts.num_bins + 1
    assert np.all(np.diff(edges) > 0)
    assert np.isclose(edges[0], ts.t0)
    assert edges[-1] >= ts.t1

def test_bin_edges_no_overshoot():
    ts = Timescale(t0=0.0, t1=1.0, bin_width=0.3)
    edges = ts.bin_edges()
    assert len(edges) == ts.num_bins + 1


def test_bin_index_flooring():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.bin_index(0.0) == 0
    assert ts.bin_index(1.9) == 0
    assert ts.bin_index(2.0) == 1
    assert ts.bin_index(9.99) == 4

def test_bin_start_end_range():
    ts = Timescale(1.0, 11.0, 2.0)
    assert ts.bin_start(0) == 1.0
    assert ts.bin_end(0) == 3.0
    assert ts.time_range(2) == (5.0, 7.0)

def test_bin_slice_clipping():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.bin_slice(-1.0, 11.0) == (0, 5)
    assert ts.bin_slice(1.0, 5.1) == (0, 3)

def test_fractional_overlap_basic():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.fractional_overlap(0.0, 2.0, 0) == 1.0
    assert ts.fractional_overlap(1.0, 2.0, 0) == 0.5
    assert ts.fractional_overlap(2.0, 4.0, 0) == 0.0
    assert ts.fractional_overlap(1.5, 2.5, 0) == 0.25
    assert ts.fractional_overlap(0.0, 2.5, 0) == 1.0

def test_fractional_overlap_clipping():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.fractional_overlap(-1.0, 1.0, 0) == 0.5
    assert ts.fractional_overlap(1.5, 4.5, 1) == 1.0


def test_bin_index_out_of_bounds():
    ts = Timescale(0.0, 10.0, 2.0)
    assert ts.bin_index(-0.1) == -1
    assert ts.bin_index(10.0) == 5  # Outside [t0, t1), but correct by floor logic

def test_bin_slice_empty_interval_produces_empty_range():
    ts = Timescale(0.0, 10.0, 2.0)
    # Even for [t, t), we get one bin covered if t falls inside a bin
    assert ts.bin_slice(5.0, 5.0) == (0, 0)

def test_fractional_overlap_outside_bin_is_zero():
    ts = Timescale(0.0, 10.0, 2.0)
    # Interval lies fully outside bin 0
    assert ts.fractional_overlap(3.0, 4.0, 0) == 0.0

def test_time_range_matches_start_end_inverse():
    ts = Timescale(0.0, 10.0, 2.0)
    for i in range(ts.num_bins):
        start = ts.bin_start(i)
        end = ts.bin_end(i)
        assert ts.time_range(i) == (start, end)