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

from .timeline import Timeline, SignalEvent
from .entity import Entity


class Boundary(Entity, Protocol):
    """
    To analyze signal "flow" in a system, we must impose a topological structure
    on the entities under observation—so that we can meaningfully speak of signals
    "flowing" from one place to another.

    A `Boundary` is a special kind of `Entity` that defines such a structure. It partitions
    signals into regions, allowing us to determine whether a given signal
    crosses the boundary (i.e., its source and target lie on opposite sides) or remains
    internal (i.e., both participants are on the same side).

    Given a history of signal events, a boundary provides the logic to assign each signal
    to a side of the partition. This enables analysis of signal propagation across arbitrary
    structural or functional or even dynamically defined partitions of the system.

    The primary purpose of a boundary is to support the study of flow dynamics:
    which signals cross it, when they do so, how long they remain within it,
    how often they enter and leave.

    While the mechanism for defining the partition is context-specific and implemented by concrete classes, the behavior
    of a boundary is formally expressed as protocol - a mapping from a `SignalLog` to a `PresenceMatrix`.

    Given a sequence of point-in-time `core.signal_log.SignalEvent` records in  `core.signal_log.SignalLog` and a finite observation window,
    a boundary produces a boolean `core.presence.PresenceMatrix` that records continuous intervals during which a signal is
    considered present within the boundary.

    This definition allows boundaries to support a rich variety of partitioning schemes—
    ranging from static partitions based on entity metadata, to dynamic signal-driven
    partitions derived entirely from signal attributes, or hybrids that combine both.

    The dynamic `PresenceMatrix` is the sole source of truth for what the "boundary" *is* at any given point in time.
    The exact structure or shape of the boundary is less important than the signal behaviors it induces—
    and those behaviors are fully determined by the boundary’s `PresenceMatrix`.
    """

    @property
    def signal_log(self) -> Timeline:
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
