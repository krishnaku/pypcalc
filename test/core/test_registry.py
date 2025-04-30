# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

import pytest
from typing import Callable, TypeVar, Dict, Generic
from core import Registry


def test_registry_register_and_create():
    registry = Registry()

    @registry.register("foo")
    def make_foo(name: str):
        return f"Foo-{name}"

    assert "foo" in registry._registry
    result = registry.create("foo", name="Bar")
    assert result == "Foo-Bar"

def test_registry_raises_on_unknown_kind():
    registry = Registry()
    with pytest.raises(ValueError, match="Unknown kind: not-registered"):
        registry.create("not-registered")
