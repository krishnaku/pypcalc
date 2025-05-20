# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Protocol, Any, Dict


class Boundary(Protocol):
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
    def id(self) -> str:
        """A stable unique identifier for the element (used for indexing and lookup)."""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """Optional key-value metadata associated with the element."""
        ...


