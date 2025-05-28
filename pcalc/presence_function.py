from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol, Callable

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

    @property
    def support(self) -> tuple[float, float]:
        return self.onset_time, self.reset_time

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
# Constant Presence
# ------------------------------

class ConstantPresence(Assertable, Bindable):
    def __init__(self, weight: float = 1.0):
        self.weight = weight

    def bind_to(self, assertion: PresenceAssertion) -> PresenceProtocol:
        t0 = assertion.start_time
        t1 = assertion.end_time
        w = self.weight

        class Impl:
            @property
            def onset_time(self) -> float:
                return t0

            @property
            def reset_time(self) -> float:
                return t1

            def overlaps(self, q0: float, q1: float) -> bool:
                return t1 > q0 and t0 < q1

            def __call__(self, q0: float, q1: float) -> float:
                if q1 <= q0 or not self.overlaps(q0, q1):
                    return 0.0
                return w * max(0.0, min(t1, q1) - max(t0, q0))

        return Impl()

# ------------------------------
# Default Presence alias
# ------------------------------

def Presence(element: Any, boundary: Any, start_time: float, end_time: float,
             asserted_by: str = "unknown", assertion_time: float = 0.0) -> PresenceAssertion:
    return ConstantPresence(weight=1.0)(
        element, boundary, start_time, end_time, asserted_by, assertion_time
    )
