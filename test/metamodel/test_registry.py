# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


import pytest
from typing import Callable, TypeVar, Dict, Generic
from sim.model import Registry


def test_registry_register_and_create():
    registry = Registry()

    @registry.register("foo")
    def make_foo(name: str):
        return f"Foo-{name}"

    assert "foo" in registry._registry
    result = registry.create(kind="foo", name="Bar")
    assert result == "Foo-Bar"

def test_registry_raises_on_unknown_kind():
    registry = Registry()
    with pytest.raises(ValueError, match="Unknown kind: not-registered"):
        registry.create(kind="not-registered")
