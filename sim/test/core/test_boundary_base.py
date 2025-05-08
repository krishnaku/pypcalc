# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from core import Signal, DomainEvent
from sim.model.boundary.base import BoundaryBase
from sim.test.mocks import MockEntity, MockSimulation

class TestBoundary(BoundaryBase):
    def on_domain_event(self, event: DomainEvent) -> None:
        pass

def make_signal(signal_id: str) -> Signal:
    return Signal(id=signal_id, name=signal_id.upper(), signal_type="test")

def make_entity(entity_id: str) -> MockEntity:
    return MockEntity(id=entity_id, name=entity_id.capitalize(), sim_context=MockSimulation())

# --- Test cases ---
def test_extract_presences_basic():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    s2 = make_signal("s2")
    log.record(entity, 1.0, "enter", s1)
    log.record(entity, 3.0, "exit", s1)
    log.record(entity, 2.0, "enter", s2)
    log.record(entity, 4.0, "exit", s2)

    presences = boundary.extract_presences(0.0, 5.0)
    assert len(presences) == 2
    assert presences[0].start == 1.0 and presences[0].end == 3.0
    assert presences[1].start == 2.0 and presences[1].end == 4.0

def test_visit_ending_before_t0():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 1.0, "enter", s1)
    log.record(entity, 2.0, "exit", s1)
    presences = boundary.extract_presences(3.0, 4.0)
    assert len(presences) == 0

def test_visit_starting_after_t1():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 3.0, "enter", s1)
    log.record(entity, 4.0, "exit", s1)
    presences = boundary.extract_presences(1.0, 2.0)
    assert len(presences) == 0

def test_visit_in_window():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 2.0, "enter", s1)
    log.record(entity, 3.0, "exit", s1)
    presences = boundary.extract_presences(1.0, 4.0)
    assert len(presences) == 1
    assert presences[0].start == 2.0 and presences[0].end == 3.0

def test_visit_starts_before_end_during_window():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 1.0, "enter", s1)
    log.record(entity, 3.0, "exit", s1)
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    # this is clipped to the window
    assert presences[0].start == 2.0 and presences[0].end == 3.0

def test_visit_starts_during_ends_after_window():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 3.0, "enter", s1)
    log.record(entity, 5.0, "exit", s1)
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    # this is clipped to the window
    assert presences[0].start == 3.0 and presences[0].end == 4.0

def test_visit_starts_before_ends_after_window():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 1.0, "enter", s1)
    log.record(entity, 5.0, "exit", s1)
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    # this is clipped to the window
    assert presences[0].start == 2.0 and presences[0].end == 4.0

def test_enter_without_exit():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 3.0, "enter", s1)
    # no exit
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    assert presences[0].start == 3.0
    assert presences[0].end == 4.0  # clipped to t1

def test_exit_without_enter():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 3.0, "exit", s1)
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    assert presences[0].start == 2.0  # t0 default
    assert presences[0].end == 3.0


def test_zero_duration_visit():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    log.record(entity, 3.0, "enter", s1)
    log.record(entity, 3.0, "exit", s1)
    presences = boundary.extract_presences(2.0, 4.0)
    assert len(presences) == 1
    # this is clipped to the window
    assert presences[0].start == 3.0 and presences[0].end == 3.0


def test_extract_presences_with_filter():
    sim = MockSimulation()
    boundary = TestBoundary("test", "B", "enter", "exit", {}, sim)
    log = boundary.timeline
    entity = make_entity("E1")
    s1 = make_signal("s1")
    s2 = make_signal("s2")
    log.record(entity, 1.0, "enter", s1)
    log.record(entity, 2.0, "enter", s2)
    log.record(entity, 3.0, "exit", s1)
    log.record(entity, 4.0, "exit", s2)

    presences = boundary.extract_presences(0.0, 5.0, match=lambda e: e.signal_id == "s1")
    assert len(presences) == 1
    assert presences[0].signal.id == "s1"