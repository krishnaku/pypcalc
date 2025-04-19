# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
#--- Generic utility class to create typed registries

from typing import TypeVar, Generic, Callable, Dict

T = TypeVar("T")
FactoryFn = Callable[..., T]

class Registry(Generic[T]):
    def __init__(self):
        self._registry: Dict[str, FactoryFn] = {}

    def register(self, kind: str) -> Callable[[FactoryFn], FactoryFn]:
        def wrapper(factory: FactoryFn) -> FactoryFn:
            self._registry[kind] = factory
            return factory
        return wrapper

    def create(self, kind: str, **kwargs) -> T:
        if kind not in self._registry:
            raise ValueError(f"Unknown kind: {kind}")
        return self._registry[kind](**kwargs)
