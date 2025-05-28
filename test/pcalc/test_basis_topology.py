# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
from sortedcontainers import SortedSet

from pcalc import Entity, PresenceAssertion, BasisTopology
from pcalc.presence import EMPTY_PRESENCE

# Sample entities
E1 = Entity("e1")
E2 = Entity("e2")
B1 = Entity("b1")
B2 = Entity("b2")


def make(pairs, e=E1, b=B1):
    return [PresenceAssertion(e, b, t0, t1) for t0, t1 in pairs]


def test_construction_and_get_cover():
    presences = make([(0, 2), (3, 4)])
    topology = BasisTopology(presences)

    cover = topology.get_cover(E1, B1)
    assert len(cover) == 2
    assert all(isinstance(p, PresenceAssertion) for p in cover)


def test_join_touching_intervals():
    p1 = PresenceAssertion(E1, B1, 0, 2)
    p2 = PresenceAssertion(E1, B1, 2, 4)
    topology = BasisTopology([p1, p2])

    result = topology.join(p1, p2)
    assert result.onset_time == 0
    assert result.reset_time == 4
    assert result.provenance == "join"


def test_join_disjoint_returns_empty():
    p1 = PresenceAssertion(E1, B1, 0, 2)
    p2 = PresenceAssertion(E1, B1, 3, 4)
    topology = BasisTopology([p1, p2])

    result = topology.join(p1, p2)
    assert result == EMPTY_PRESENCE


def test_closure_merges_adjacent():
    presences = make([(0, 2), (2, 4), (5, 6)])
    topology = BasisTopology(presences)

    closed = topology.closure()
    assert len(closed) == 2  # [(0, 4), (5, 6)]
    assert any(p.onset_time == 0 and p.reset_time == 4 for p in closed)
    assert any(p.onset_time == 5 and p.reset_time == 6 for p in closed)


def test_find_overlapping_within_cover():
    presences = make([(0, 2), (1, 3), (4, 6)])
    topology = BasisTopology(presences)

    target = PresenceAssertion(E1, B1, 1.5, 4.5)
    overlaps = topology.find_overlapping(target)

    expected = {(0, 2), (1, 3), (4, 6)}
    actual = {(p.onset_time, p.reset_time) for p in overlaps}
    assert actual == expected

def test_multiple_covers_are_separate():
    p1 = PresenceAssertion(E1, B1, 0, 2)
    p2 = PresenceAssertion(E1, B2, 1, 3)
    p3 = PresenceAssertion(E2, B1, 2, 4)
    topology = BasisTopology([p1, p2, p3])

    assert len(topology.get_cover(E1, B1)) == 1
    assert len(topology.get_cover(E1, B2)) == 1
    assert len(topology.get_cover(E2, B1)) == 1


def test_closure_respects_cover_boundaries():
    presences = (
        make([(0, 2), (2, 4)], e=E1, b=B1) +
        make([(1, 3), (3, 5)], e=E2, b=B1)
    )
    topology = BasisTopology(presences)
    closed = topology.closure()

    expected = {
        PresenceAssertion(E1, B1, 0, 4, provenance="join"),
        PresenceAssertion(E2, B1, 1, 5, provenance="join")
    }
    assert closed == expected


def test_join_between_different_covers_returns_empty():
    p1 = PresenceAssertion(E1, B1, 0, 2)
    p2 = PresenceAssertion(E2, B1, 1, 3)
    topology = BasisTopology([p1, p2])

    joined = topology.join(p1, p2)
    assert joined == EMPTY_PRESENCE


def test_find_overlapping_only_searches_within_cover():
    p1 = PresenceAssertion(E1, B1, 0, 2)
    p2 = PresenceAssertion(E1, B2, 1, 3)
    p3 = PresenceAssertion(E2, B1, 2, 4)
    topology = BasisTopology([p1, p2, p3])

    target = PresenceAssertion(E1, B1, 1.5, 2.5)
    overlaps = topology.find_overlapping(target)

    assert overlaps == [p1]


def test_get_cover_missing_returns_empty():
    topology = BasisTopology([])
    cover = topology.get_cover(Entity("ghost"), Entity("phantom"))
    assert cover == SortedSet([])
