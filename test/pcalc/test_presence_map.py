# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar


import numpy as np
from metamodel import Presence

from pcalc import PresenceMap, Timescale
from test.mocks import MockElement, MockBoundary

dummy_boundary = MockBoundary()

def test_full_overlap_single_bin():
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)
    p = Presence(boundary=dummy_boundary, element=MockElement(), start=1.0, end=2.0)
    pm = PresenceMap(p, ts)
    assert pm.is_mapped
    assert pm.start_bin == 1
    assert pm.end_bin == 2
    assert pm.start_value == 1.0
    assert pm.end_value == 1.0

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
    assert np.isclose(pm.end_value, 0.3)
