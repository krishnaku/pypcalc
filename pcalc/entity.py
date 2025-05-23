# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
## Introduction

In the Presence Calculus, we assume that we are operating over some externally
defined domain $D$ with its own structure, topologies, constraints, and
semantics. While these aspects of the domain influence the kinds of presence
assertions that can be expressed over it, the presence calculus itself is domain-agnostic.

It is solely concerned with presence assertions over the domain, which are
assumed as given, and the derived constructs and calculations thereof under
the calculus.

The connection between the domain and the calculus is established via the
`EntityProtocol`, which declares the minimal contract a member of the domain
$D$ must satisfy in order to participate in presence assertions over $D$.

Since a [presence assertion](./presence.html)  is a statement of the form "an element was present
in a boundary from time $t_0$ to $t_1$", it is useful to think of Elements ($E$)
and Boundaries ($B$) as distinguished subsets of a shared domain of entities:

- Some entities act as "things" that are present (Elements).
- Others act as "places" or contexts in which presence occurs (Boundaries).

$$
E = \{ e_1, e_2, \dots, e_n \} \subset D
$$

$$
B = \{ b_1, b_2, \dots, b_m \} \subset D
$$

There are no constraints on what an element or boundary can be. These roles
are application-defined, context-dependent, and scoped to a particular set of
presence assertions under analysis.

## Examples

- In traffic network, the locations and
road segments of the road network might be natural boundaries and vehicles might be elements.

- In a business value network, the roles in the network would be natural boundaries and value exchanges
between the roles would be natural elements.

- In a customer relationship management context, the boundaries might be customer segments and elements might be customers
or prospects.

- In a process management context, the boundaries might be process states and the elements might be processing items.

- In an organizational design context, the organization units might be the boundaries and the elements might be job functions.

Please note that these are illustrative examples.

In general, you are free to model elements and boundaries as you wish, provided that
there are meaningful domain semantics you can assign to a statement
like "An element was in a boundary from time $t_0$ to $t_1$".

## Structure

This module defines the minimal contract and implementation required for an
Entity to participate in a presence assertion, either as an Element or as
a Boundary.
"""
from __future__ import annotations

import uuid
from typing import Protocol, runtime_checkable, Dict, Any, Optional


@runtime_checkable
class EntityProtocol(Protocol):
    """
    The interface contract for a domain entity to participate in a presence assertion.

    Each entity requires only a unique identifier, a user-facing name.

    Optional metadata may be provided and exposes specific attributes of the domain
    entities that are relevant to the *interpreting* the results of analyzing presence.

    They are not necessary for any of the core calculations or results of the calculus.
    """
    __init__ = None  # type: ignore

    @property
    def id(self) -> str:
        """
        A stable, unique identifier for the entity.
        Used for indexing and identity.
        Defaults to a uuid.uuid4().
        """
        ...

    @property
    def name(self) -> str:
        """
        A user facing name for the entity, defaults to the id if None.
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


class EntityMixin:
    """A mixin class that can be used to inject common shared behavior
    of objects satisfying the EntityProtocol  into existing domain entities.
    """

    def summary(self: EntityProtocol) -> str:
        """
        Return a human-readable summary based on id and metadata.
        """
        meta = getattr(self, "metadata", {})
        if not meta:
            return f"Element[{self.id}] name = {self.name} (no metadata)"
        formatted = ", ".join(f"{k}={v!r}" for k, v in meta.items())
        return f"Element[{self.id}] name = {self.name} {{{formatted}}}"


class EntityView(EntityMixin):
    """A view class that allows domain objects to behave like entities"""

    __slots__ = ("_id", "_name", "_metadata")

    def __init__(self, base: EntityProtocol):
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


class Entity(EntityMixin, EntityProtocol):
    """A default implementation of fully functional element."""

    __slots__ = ("_id", "_name", "_metadata")

    # noinspection PyProtocol
    def __init__(self, id: Optional[str] = None, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
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
