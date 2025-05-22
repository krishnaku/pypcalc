# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
A *Boundary* is a place, defined region, location, or container for elements in
the domain. It is best thought of as an abstract context for a presence
assertion.

The Presence Calculus is agnostic to the nature of boundaries, treating them as
opaque members of a set of entities in some underlying domain $D$:

$$
B = \\\{ b_1, b_2, \dots, b_n \\\} \subset D
$$

Examples of boundaries include physical locations or organizational units in a
business domain, process states in a process domain, communication channels in
a messaging domain, or actors and actants in an actor domain.

In general, there are no constraints on what a boundary can be—it depends
entirely on what you choose to model with presence assertions over $D$.
It is best to think of boundaries as playing the "place" role in a presence
assertion. The same domain entity may appear in both boundary and element
roles.

Each boundary requires only a unique identifier, a user-facing name, and
optional metadata that can be used to filter or aggregate presences and
derived metrics.

This module contains the contract and implementations for a Boundary.
"""

from __future__ import annotations

import uuid
from typing import Protocol, runtime_checkable, Dict, Any, Optional


@runtime_checkable
class BoundaryProtocol(Protocol):
    """The structural contract for a Boundary"""

    @property
    def id(self) -> str:
        """
        A stable, unique identifier for the element.
        Used for indexing and identity.
        Defaults to a uuid.uuid4().
        """
        ...

    @property
    def name(self) -> str:
        """
        A user facing name for the element, defaults to the id if None.
        """
        ...

    @name.setter
    def name(self, name: str) -> None:
        """Setter for name"""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Optional extensible key-value metadata.
        """
        ...


class BoundaryMixin:
    """A mixin class that can be used to inject common shared behavior
        of elements.
    """

    def summary(self: BoundaryProtocol) -> str:
        """
        Return a human-readable summary based on id and metadata.
        """
        meta = getattr(self, "metadata", {})
        if not meta:
            return f"Boundary[{self.id}] name = {self.name} (no metadata)"
        formatted = ", ".join(f"{k}={v!r}" for k, v in meta.items())
        return f"Boundary[{self.id}] name = {self.name} {{{formatted}}}"


class BoundaryView(BoundaryMixin):
    """A view class that allows domain objects to behave like elements"""

    __slots__ = ("_id", "_name", "_metadata")

    def __init__(self, base: BoundaryProtocol):
        self._base = base

    @property
    def id(self) -> str:
        return self._base.id

    @property
    def name(self) -> Optional[str]:
        return self._base.name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._base.metadata


class Boundary(BoundaryMixin, BoundaryProtocol):
    """A default implementation of fully functional boundary."""

    __slots__ = ("_id", "_name", "_metadata")

    def __init__(self, id: Optional[str] = None, name: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        self._id: str = id or str(uuid.uuid4())
        self._name: str = name or self.id
        self._metadata: Dict[str, Any] = metadata or {}

    @property
    def id(self) -> str:
        return self._id

    # noinspection PyProtocol
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def __str__(self) -> str:
        return self.summary()
