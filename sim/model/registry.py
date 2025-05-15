# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


"""
This module defines a lightweight  generic`Registry` class that maps string keys to factory functions.
It is useful for building extensible systems where new types or behaviors can be plugged in
via decorators and selected dynamically at runtime.

### Example Usage

```python
# from module sim.model.delay

from core import Registry
from sim.model.delay.protocol import DelayBehavior
# create a registry for delay behaviors
delay_behavior_registry: Registry[DelayBehavior]= Registry()

# register behaviors with their constructors from `sim.model.delay.behavior`
@delay_behavior_registry.register("Exponential Delay")
class ExponentialDelay(DelayBehaviorBase):
    def __init__(self, sim_context, avg_delay=None):
        if avg_delay is None:
            raise ValueError("Exponential Delay must specify a non null value for the parameter delay")
        super().__init__(sim_context, avg_delay)

    def delay(self) -> Generator[simpy.Event, None, None]:
        delay = random.expovariate(self._avg_delay)
        yield self._sim_context.timeout(delay)


# Later, instantiate from string
delay_behavior = delay_behavior_registry.create("Exponential Delay", avg_delay=1.5)
```
This pattern avoids large if-else or switch-case blocks and makes it easy to register new behaviors
without modifying existing logic.

We use this pattern extensively in this code base as a universal object factory.
"""

from typing import TypeVar, Generic, Callable, Dict

T = TypeVar("T")
FactoryFn = Callable[..., T]

class Registry(Generic[T]):
    """A generic registry for mapping string keys to factory functions or class constructors."""

    def __init__(self):
        """Initialize an empty registry."""
        self._registry: Dict[str, FactoryFn] = {}

    def register(self, kind: str) -> Callable[[FactoryFn], FactoryFn]:
        """
        Decorator to register a factory function under the given key.

        Args:
            kind: A string identifier for the registered type.

        Returns:
            A decorator that registers the factory and returns it unchanged.
        """

        def wrapper(factory: FactoryFn) -> FactoryFn:
            self._registry[kind] = factory
            return factory

        return wrapper

    def create(self, kind: str = None, **kwargs) -> T:
        """
        Instantiate a registered object by kind.

        Args:
            kind: The string key under which the factory was registered.
            **kwargs: Arguments passed to the factory function.

        Returns:
            An instance of the registered type.

        Raises:
            ValueError: If the given kind is not registered.
        """
        if kind not in self._registry:
            raise ValueError(f"Unknown kind: {kind}")
        return self._registry[kind](**kwargs)

