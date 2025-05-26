# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT



import pytest
from fontTools.merge.util import avg_int

from pcalc import Presence, Entity, BasisTopology
from pcalc.presence_invariant import PresenceInvariant

dummy = Entity()

def make_presences():
    boundary = Entity()

    return [
        Presence(Entity(), boundary, 0.0, 1.0),
        Presence(Entity(), boundary, 1.0, 2.0),
        Presence(Entity(), boundary, 3.0, 4.0),
        Presence(Entity(), boundary, 4.6, float("inf")),
    ]


@pytest.mark.parametrize("case, start, end, expected", [
    ("Only first presence in [0.0, 1.0)", 0.0, 1.0, 1.0),
    ("First two presences in [0.0, 2.5)", 0.0, 2.5, 0.8),
    ("Only third presence in [3.0, 4.0)", 3.0, 4.0, 1.0),
    ("Only open-ended presence in [4.6, 5.5)", 4.6, 5.5, 1 / 0.9),
    ("Zero-length window [2.0, 2.0)", 2.0, 2.0, 0.0),
    ("All presences in [0.0, 6.0)", 0.0, 6.0, 4.0 / 6.0),
    ("Edge overlap only with last (inf) presence [5.9, 6.0)", 5.9, 6.0, 1 / 0.1),
])
def test_incidence_rate(case, start, end, expected):
    presences = make_presences()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.incidence_rate(start, end)
    assert abs(actual - expected) < 1e-6, case


@pytest.mark.parametrize("case, start, end, expected", [
    ("First presence only", 0.0, 1.0, 1.0),
    ("All presences", 0.0, 6.0, 1.1),
    ("Middle region [2.0, 4.0)", 2.0, 4.0, 1.0),
    ("Open-ended clipped [4.5, 6.0)", 4.5, 6.0, 1.4),
])
def test_avg_presence_mass(case, start, end, expected):
    presences = make_presences()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.avg_presence_mass(start, end)
    assert abs(actual - expected) < 1e-6, case


@pytest.mark.parametrize("case, start, end, expected", [
    ("First presence only", 0.0, 1.0, 1.0),
    ("All presences", 0.0, 6.0, 4.4 / 6.0),
    ("Middle region [2.0, 4.0)", 2.0, 4.0, 1.0 / 2.0),
    ("Open-ended clipped [4.5, 6.0)", 4.5, 6.0, 1.4 / 1.5),
])
def test_avg_presence_density(case, start, end, expected):
    presences = make_presences()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.avg_presence_density(start, end)
    assert abs(actual - expected) < 1e-6, case


@pytest.mark.parametrize("start, end", [
    (0.0, 6.0),
    (0.0, 1.0),
    (1.0, 2.0),
    (4.6, 5.5),
    (2.0, 4.0),
])
def test_presence_invariant(start, end):
    presences = make_presences()
    topology = BasisTopology(presences)
    invariant = PresenceInvariant(topology)
    incidence_rate = invariant.incidence_rate(start, end)
    avg_mass = invariant.avg_presence_mass(start, end)
    avg_density = invariant.avg_presence_density(start, end)

    # Check invariant: avg_mass == incidence * flow_rate
    lhs = avg_density
    rhs = incidence_rate * avg_mass
    assert abs(lhs - rhs) < 1e-6, f"Invariant failed for [{start}, {end}): {lhs} != {rhs}"

def make_presences_with_non_trivial_closure():
    boundary = Entity()

    e1 = Entity()
    e2 = Entity()
    return [
        # The two presences of e1 will be joined
        Presence(e1, boundary, 0.0, 1.0),
        Presence(e1, boundary, 1.0, 2.0),
        # The two presences of e2 will stay separate
        Presence(e2, boundary, 3.0, 4.0),
        Presence(e2, boundary, 4.6, float("inf")),
    ]


@pytest.mark.parametrize("case, start, end, expected", [
    ("Only first presence in [0.0, 1.0)", 0.0, 1.0, 1 / 1),
    ("First two presences in [0.0, 2.5)", 0.0, 2.5, 1/2.5),
    ("Only third presence in [3.0, 4.0)", 3.0, 4.0, 1/1),
    ("Only open-ended presence in [4.6, 5.5)", 4.6, 5.5, 1 / 0.9),
    ("Zero-length window [2.0, 2.0)", 2.0, 2.0, 0.0),
    ("All presences in [0.0, 6.0)", 0.0, 6.0, 3.0 / 6.0),
    ("Edge overlap only with last (inf) presence [5.9, 6.0)", 5.9, 6.0, 1 / 0.1),
])
def test_incidence_rate_under_closure(case, start, end, expected):
    presences = make_presences_with_non_trivial_closure()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.incidence_rate(start, end)
    assert abs(actual - expected) < 1e-6, case


@pytest.mark.parametrize("case, start, end, expected", [
    ("First presence only", 0.0, 1.0, 1.0),
    ("All presences", 0.0, 6.0, 4.4/3.0),
    ("Middle region [2.0, 4.0)", 2.0, 4.0, 1.0),
    ("Open-ended clipped [4.5, 6.0)", 4.5, 6.0, 1.4),
])
def test_avg_presence_mass_under_closure(case, start, end, expected):
    presences = make_presences_with_non_trivial_closure()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.avg_presence_mass(start, end)
    assert abs(actual - expected) < 1e-6, case

@pytest.mark.parametrize("case, start, end, expected", [
    ("First presence only", 0.0, 1.0, 1.0),
    ("All presences", 0.0, 6.0, 4.4 / 6.0),
    ("Middle region [2.0, 4.0)", 2.0, 4.0, 1.0 / 2.0),
    ("Open-ended clipped [4.5, 6.0)", 4.5, 6.0, 1.4 / 1.5),
])
def test_avg_presence_density_under_closure(case, start, end, expected):
    presences = make_presences_with_non_trivial_closure()
    topology = BasisTopology(presences)
    metrics = PresenceInvariant(topology)
    actual = metrics.avg_presence_density(start, end)
    assert abs(actual - expected) < 1e-6, case

@pytest.mark.parametrize("start, end", [
    (0.0, 6.0),
    (0.0, 1.0),
    (1.0, 2.0),
    (4.6, 5.5),
    (2.0, 4.0),
])
def test_presence_invariant_under_closure(start, end):
    presences = make_presences_with_non_trivial_closure()
    topology = BasisTopology(presences)
    invariant = PresenceInvariant(topology)
    incidence_rate = invariant.incidence_rate(start, end)
    avg_mass = invariant.avg_presence_mass(start, end)
    avg_density = invariant.avg_presence_density(start, end)

    # Check invariant: avg_mass == incidence * flow_rate
    lhs = avg_density
    rhs = incidence_rate * avg_mass
    assert abs(lhs - rhs) < 1e-6, f"Invariant failed for [{start}, {end}): {lhs} != {rhs}"