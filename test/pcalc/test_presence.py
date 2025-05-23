# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np

from pcalc import Presence, Element


def test_overlap_true():
    p = Presence("x", Element(), 1.0, 5.0)
    assert p.overlaps(2.0, 4.0) is True
    assert p.overlaps(4.9, 6.0) is True
    assert p.overlaps(0.0, 1.1) is True

def test_overlap_false():
    p = Presence("x", Element(), 1.0, 5.0)
    assert p.overlaps(5.0, 6.0) is False
    assert p.overlaps(0.0, 1.0) is False


def test_duration():
    p = Presence("x", Element(), 1.0, 4.0)
    assert p.duration() == 3.0

def test_duration_inf():
    p = Presence("x", Element(), 1.0, np.inf)
    assert p.duration() == np.inf

def test_residence_time_overlap():
    p = Presence("x", Element(), 1.0, 5.0)
    assert p.residence_time(2.0, 6.0) == 3.0

def test_residence_time_no_overlap():
    p = Presence("x", Element(), 1.0, 2.0)
    assert p.residence_time(2.0, 3.0) == 0.0

def test_str_representation():
    p = Presence("x", Element("B"), 3.0, 7.0, "observed")
    s = str(p)
    assert "Presence(element=x, boundary=Element[B] name = B (no metadata), interval=[3.0, 7.0), provenance=observed)" in s
