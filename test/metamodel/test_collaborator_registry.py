# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


from sim.model.collaborator import collaborator_registry, Requestor, Responder
from test.mocks import MockSimulation

def test_requestor_and_responder_are_registered():
    assert "Requestor" in collaborator_registry._registry
    assert "Responder" in collaborator_registry._registry


def test_create_requestor_and_responder():
    sim = MockSimulation()

    requestor = collaborator_registry.create(
        kind="Requestor",
        name="req1",
        domain_context=sim,
        delay_behavior=dict(kind="Deterministic", avg_delay=0.0)
    )
    assert isinstance(requestor, Requestor)
    assert requestor.name == "req1"
    assert requestor.metadata == dict(
        concurrency=None,
        delay_behavior=dict(kind="Deterministic", avg_delay=0.0)
    )

    responder = collaborator_registry.create(
        kind="Responder",
        name="res1",
        domain_context=sim,
        delay_behavior=dict(kind="Deterministic", avg_delay=0.0)
    )
    assert isinstance(responder, Responder)
    assert responder.name == "res1"
    assert responder.metadata == dict(
        concurrency=None,
        delay_behavior=dict(kind="Deterministic", avg_delay=0.0)
    )
