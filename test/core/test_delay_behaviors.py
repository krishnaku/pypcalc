# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import pytest
import simpy
from sim.model.delay import delay_behavior_registry
from sim.model.delay.behavior import ExponentialDelay, Deterministic, Markov

@pytest.fixture
def sim_context():
    return simpy.Environment()


def test_delay_behaviors_registered():
    assert "Deterministic" in delay_behavior_registry._registry
    assert "Exponential Delay" in delay_behavior_registry._registry
    assert "Markov" in delay_behavior_registry._registry


def test_create_deterministic(sim_context):
    behavior = delay_behavior_registry.create("Deterministic", sim_context=sim_context, avg_delay=3)
    assert isinstance(behavior, Deterministic)

    event = behavior.delay()
    timeout = next(event)
    assert isinstance(timeout, simpy.events.Timeout)
    assert timeout._delay == 3


def test_create_exponential(sim_context):
    behavior = delay_behavior_registry.create("Exponential Delay", sim_context=sim_context, avg_delay=2)
    assert isinstance(behavior, ExponentialDelay)

    event = behavior.delay()
    timeout = next(event)
    assert isinstance(timeout, simpy.events.Timeout)
    # Can't assert exact delay because it's random, but it should be > 0
    assert timeout._delay > 0


@pytest.mark.parametrize("kwargs, expected_delay", [
    ({"mean_time_between_arrivals": 5}, 5),
    ({"avg_processing_time": 4}, 4),
    ({"mean_time_between_requests": 3}, 3),
    ({"avg_delay": 2}, 2),
])
def test_create_markov(sim_context, kwargs, expected_delay):
    behavior = delay_behavior_registry.create("Markov", sim_context=sim_context, **kwargs)
    assert isinstance(behavior, Markov)

    event = behavior.delay()
    timeout = next(event)
    assert isinstance(timeout, simpy.events.Timeout)
    assert timeout._delay > 0
