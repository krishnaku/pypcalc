# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol, Callable, Union
from abc import ABC, abstractmethod

# ------------------------------
# Protocols
# ------------------------------

class PresenceProtocol(Protocol):
    def __call__(self, t0: float, t1: float) -> float: ...
    def overlaps(self, t0: float, t1: float) -> bool: ...
    @property
    def onset_time(self) -> float: ...
    @property
    def reset_time(self) -> float: ...

class Bindable(Protocol):
    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol: ...

# ------------------------------
# Presence Assertion
# ------------------------------

@dataclass
class PresenceAssertion:
    element: Any
    boundary: Any
    start_time: float
    end_time: float
    presence: PresenceProtocol
    asserted_by: str = "unknown"
    assertion_time: float = 0.0

    @property
    def onset_time(self) -> float:
        return self.presence.onset_time

    @property
    def reset_time(self) -> float:
        return self.presence.reset_time

    def mass(self) -> float:
        return self.presence(self.onset_time, self.reset_time)

    def overlaps(self, t0: float, t1: float) -> bool:
        return self.presence.overlaps(t0, t1)

    def mass_contribution(self, t0: float, t1: float) -> float:
        return self.presence(t0, t1)

# ------------------------------
# Mixin for Function Call
# ------------------------------

class Assertable:
    def __call__(
        self: Bindable,
        element: Any,
        boundary: Any,
        start_time: float,
        end_time: float,
        asserted_by: str = "unknown",
        assertion_time: float = 0.0,
    ) -> PresenceAssertion:
        temp = PresenceAssertion(
            element=element,
            boundary=boundary,
            start_time=start_time,
            end_time=end_time,
            presence=None,  # temporarily None
            asserted_by=asserted_by,
            assertion_time=assertion_time,
        )
        temp.presence = self.bind_to(temp)
        return temp

# ------------------------------
# Composable Base Class
# ------------------------------

class ComposablePresence(Bindable, Assertable, ABC):

    @abstractmethod
    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        ...

    def __add__(self, other: ComposablePresence) -> ComposablePresence:
        return BinaryOpPresence(self, other, op=lambda a, b: a + b)

    def __mul__(self, other: Union[float, ComposablePresence]) -> ComposablePresence:
        if isinstance(other, (int, float)):
            return ScalarOpPresence(self, scalar=other, op=lambda a, s: a * s)
        return BinaryOpPresence(self, other, op=lambda a, b: a * b)

    def __pow__(self, exponent: float) -> ComposablePresence:
        return ScalarOpPresence(self, scalar=exponent, op=lambda a, e: a ** e)

    def compose(self, inner: ComposablePresence) -> ComposablePresence:
        return ComposedPresence(self, inner)

# ------------------------------
# Constant Presence
# ------------------------------

class ConstantPresence(ComposablePresence):
    def __init__(self, weight: float = 1.0):
        self.weight = weight

    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        t0, t1 = assertion.start_time, assertion.end_time
        w = self.weight

        class Impl:
            @property
            def onset_time(self) -> float: return t0
            @property
            def reset_time(self) -> float: return t1

            def overlaps(self, q0: float, q1: float) -> bool:
                return t1 > q0 and t0 < q1

            def __call__(self, q0: float, q1: float) -> float:
                if q1 <= q0 or not self.overlaps(q0, q1): return 0.0
                return w * (min(t1, q1) - max(t0, q0))

        return Impl()

# ------------------------------
# Composed Presence f(g(x))
# ------------------------------

class ComposedPresence(ComposablePresence):
    def __init__(self, outer: ComposablePresence, inner: ComposablePresence):
        self.outer = outer
        self.inner = inner

    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        inner_assertion = self.inner(
            assertion.element, assertion.boundary,
            assertion.start_time, assertion.end_time,
            asserted_by=assertion.asserted_by,
            assertion_time=assertion.assertion_time
        )
        outer_assertion = self.outer(
            assertion.element, assertion.boundary,
            inner_assertion.onset_time, inner_assertion.reset_time,
            asserted_by=assertion.asserted_by,
            assertion_time=assertion.assertion_time
        )
        return outer_assertion.presence

# ------------------------------
# Scalar Operation f(x) * c or f(x) ** p
# ------------------------------

class ScalarOpPresence(ComposablePresence):
    def __init__(self, base: ComposablePresence, scalar: float, op: Callable[[float, float], float]):
        self.base = base
        self.scalar = scalar
        self.op = op

    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        base_presence = self.base.bind_to(assertion)

        class Impl:
            @property
            def onset_time(self) -> float: return base_presence.onset_time
            @property
            def reset_time(self) -> float: return base_presence.reset_time

            def overlaps(self, q0: float, q1: float) -> bool:
                return base_presence.overlaps(q0, q1)

            def __call__(self, q0: float, q1: float) -> float:
                return self.op(base_presence(q0, q1), self.scalar)

        return Impl()

# ------------------------------
# Binary Operation f(x) + g(x) or f(x) * g(x)
# ------------------------------

class BinaryOpPresence(ComposablePresence):
    def __init__(self, f1: ComposablePresence, f2: ComposablePresence, op: Callable[[float, float], float]):
        self.f1 = f1
        self.f2 = f2
        self.op = op

    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        p1 = self.f1.bind_to(assertion)
        p2 = self.f2.bind_to(assertion)

        class Impl:
            @property
            def onset_time(self) -> float: return min(p1.onset_time, p2.onset_time)
            @property
            def reset_time(self) -> float: return max(p1.reset_time, p2.reset_time)

            def overlaps(self, q0: float, q1: float) -> bool:
                return self.onset_time < q1 and self.reset_time > q0

            def __call__(self, q0: float, q1: float) -> float:
                return self.op(p1(q0, q1), p2(q0, q1))

        return Impl()

# ------------------------------
# Default Presence alias
# ------------------------------

def Presence(element: Any, boundary: Any, start_time: float, end_time: float,
             asserted_by: str = "unknown", assertion_time: float = 0.0) -> PresenceAssertion:
    return ConstantPresence(weight=1.0)(
        element, boundary, start_time, end_time, asserted_by, assertion_time
    )
