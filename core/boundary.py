# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

from typing import List, Protocol, TYPE_CHECKING

from .presence import Presence, PresenceMatrix

if TYPE_CHECKING:
    pass

from .timeline import Timeline, DomainEvent
from .entity import Entity


class Boundary(Entity, Protocol):
    """
    To analyze signal "flow" in a domain, we must impose a topological structure
    on the domain elements under observation, so that we can meaningfully speak of "place" and "time" in the domain.

    A `Boundary` is a special kind of `Entity` that defines such a structure. It partitions
    a domain into regions, potentially, each with its own timeline.

    Given domain events in a timeline, a boundary determines whether elements of the domain - entities, signals,
    transactions, etc. are "present" in the boundary or not, at a particular moment in time.

    The primary purpose of a boundary is to support the study of flow dynamics:
    which domain elements cross a boundary, when they do so, how long they remain within it,
    how often they enter and leave.

    This is the foundation for analyzing "flow" in the domain.

    The behavior of a boundary is formally expressed as protocol - a mapping from a `Timeline` to a `PresenceMatrix`.

    Given a sequence of point-in-time `core.timeline.DomainEvent` records in  `core.timeline.Timeline` and a finite observation window,
    a boundary produces a boolean `core.presence.PresenceMatrix` that records continuous intervals during which a domain element is
    considered present within the boundary.

    This definition allows boundaries to support a rich variety of partitioning behavior —
    ranging from static partitions based on entity metadata, to dynamic signal-driven
    partitions derived entirely from signal attributes, or hybrids that combine both.

    The dynamic `PresenceMatrix` is the sole source of truth for what the "boundary" *is* at any given point in time.
    The exact structure or shape of the boundary is less important than the flow behaviors it induces—
    and those behaviors are fully determined by the boundary’s `PresenceMatrix`.

    Concrete implementation of the `Boundary` are responsible for determining the `PresenceMatrix` for boundary.
    """

    @property
    def timeline(self) -> Timeline:
        """The `SignalLog` associated with this boundary, capturing events that crossed it."""
        ...

    def get_presence_matrix(self, start_time: float, end_time: float, bin_width: float) -> PresenceMatrix:
        """
        Compute a presence matrix summarizing signal activity within the boundary over a time window.

        Args:
            start_time: The beginning of the observation window.
            end_time: The end of the observation window.
            bin_width: The width of each time bin for bucketing presence data.

        Returns:
            A `PresenceMatrix` that captures which entities were present in the boundary across time.
        """
        ...
