# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np

from pcalc import Presence, Boundary


def test_overlap_true():
    p = Presence("x", Boundary(), 1.0, 5.0)
    assert p.overlaps(2.0, 4.0) is True
    assert p.overlaps(4.9, 6.0) is True
    assert p.overlaps(0.0, 1.1) is True

def test_overlap_false():
    p = Presence("x", Boundary(), 1.0, 5.0)
    assert p.overlaps(5.0, 6.0) is False
    assert p.overlaps(0.0, 1.0) is False

def test_clip_overlap():
    p = Presence("x", Boundary(), 1.0, 5.0)
    clipped = p.clip(2.0, 4.0)
    assert clipped is not None
    assert clipped.start == 2.0
    assert clipped.end == 4.0
    assert "clipped from" in clipped.provenance

def test_clip_no_overlap():
    p = Presence("x", Boundary(), 1.0, 5.0)
    clipped = p.clip(5.0, 6.0)
    assert clipped is None

def test_duration():
    p = Presence("x", Boundary(), 1.0, 4.0)
    assert p.duration() == 3.0

def test_duration_inf():
    p = Presence("x", Boundary(), 1.0, np.inf)
    assert p.duration() == np.inf

def test_residence_time_overlap():
    p = Presence("x", Boundary(), 1.0, 5.0)
    assert p.residence_time(2.0, 6.0) == 3.0

def test_residence_time_no_overlap():
    p = Presence("x", Boundary(), 1.0, 2.0)
    assert p.residence_time(2.0, 3.0) == 0.0

def test_str_representation():
    p = Presence("x", Boundary("B"), 3.0, 7.0, "observed")
    s = str(p)
    assert "Presence(element=x, boundary=Boundary[B] name = B (no metadata), interval=[3.0, 7.0), provenance=observed)" in s
