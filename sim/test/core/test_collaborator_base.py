# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

import pytest
from sim.test.mocks import MockSimulation
from sim.test.assertions import sim_log, SignalAssertion, SignalLogAssertion
from sim.model.collaborator.base import CollaboratorBase, Request, Response


class MockCollaborator(CollaboratorBase):
    def __init__(self, name, sim_context, concurrency=None):
        super().__init__(name, sim_context, concurrency)
        self.received_requests = []
        self.received_responses = []
        self.start_process_called = False

    def start_processes(self):
        self.start_process_called = False


    def on_receive_request(self, request: Request):
        self.received_requests.append(request)
        self.transactions_in_process.add(request.transaction.id)
        yield self.sim_context.timeout(1)

    def on_receive_response(self, response: Response):
        self.received_responses.append(response)
        self.transactions_in_process.remove(response.transaction.id)
        yield self.sim_context.timeout(0)


@pytest.fixture
def sim():
    return MockSimulation()


def test_send_and_receive(sim):
    a = MockCollaborator("A", sim)
    b = MockCollaborator("B", sim)
    a.set_peer(b)

    request = Request("req-1")
    a.send(request)

    assert len(b.inbox.items) == 1
    assert isinstance(b.inbox.items[0], Request)
    assert b.inbox.items[0].name == "req-1"


def test_receive_and_process(sim):
    a = MockCollaborator("A", sim)
    b = MockCollaborator("B", sim)
    a.set_peer(b)

    # Send request from b to a
    b.send(Request("req-1"))
    sim.process(a.receive())
    sim.run(until=2)

    # It should have processed and responded to the request
    assert len(a.received_requests) == 1
    assert a.received_requests[0].name == "req-1"
    assert len(b.inbox.items) == 1
    assert isinstance(b.inbox.items[0], Response)

def test_send_logs_signal(sim):
    a = MockCollaborator("A", sim)
    b = MockCollaborator("B", sim)
    a.set_peer(b)

    request = Request("req-1")
    a.send(request)

    sim.run(until=1)

    sig: SignalAssertion = sim_log(sim).latest_timeline().signal_at(0)
    assert sig.has_source("A")
    assert sig.has_target("B")
    assert sig.has_signal("req-1")




def test_request_response_is_logged(sim):
    a = MockCollaborator("A", sim)
    b = MockCollaborator("B", sim)
    a.set_peer(b)

    # Send request from B to A
    request = Request("req-1")
    b.send(request)  # b → a

    # Confirm peer inbox received it
    assert len(a.inbox.items) == 1
    assert isinstance(a.inbox.items[0], Request)

    # Start A's receive coroutine
    sim.process(a.receive())

    # Run the simulation
    sim.run(until=5)

    # Inspect the signal log
    logs: SignalLogAssertion = sim_log(sim).latest_timeline()
    assert logs.has_length(3)

    # Collaboration protocol
    assert logs.contains_event( signal_type="request", signal_name="req-1",  event_type="send", source='B', target='A', count=1)
    assert logs.contains_event( signal_type="request", signal_name="req-1", event_type="receive", source='A', target='B', count=1)
    assert logs.contains_event( signal_type="response", signal_name="req-1",  event_type="send", source='A', target='B', count=1)


def test_concurrency_tracking(sim):
    c = MockCollaborator("C", sim, concurrency=1)
    dummy_request = Request("req-1")

    # simulate dispatch with and without resource
    gen = c.dispatch(dummy_request)
    sim.process(gen)
    sim.run(until=1)

    assert c.signals_in_process == 0  # properly decremented after dispatch
