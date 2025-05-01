# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from sim.model.collaborator import collaborator_registry, Requestor, Responder
from sim.test.mocks import MockSimulation

def test_requestor_and_responder_are_registered():
    assert "Requestor" in collaborator_registry._registry
    assert "Responder" in collaborator_registry._registry


def test_create_requestor_and_responder():
    sim = MockSimulation()

    requestor = collaborator_registry.create(
        "Requestor",
        name="req1",
        sim_context=sim,
        delay_behavior=dict(type="Deterministic", avg_delay=0.0)
    )
    assert isinstance(requestor, Requestor)
    assert requestor.name == "req1"

    responder = collaborator_registry.create(
        "Responder",
        name="res1",
        sim_context=sim,
        delay_behavior=dict(type="Deterministic", avg_delay=0.0)
    )
    assert isinstance(responder, Responder)
    assert responder.name == "res1"
