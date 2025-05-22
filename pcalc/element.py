# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
An *Element* is a thing in the domain—typically a noun, and the subject of
presence assertions.

The Presence Calculus is agnostic to the nature of elements, treating them as
opaque members of a set of entities in some underlying domain $D$:

$$
E = \\\{ e_1, e_2, \dots, e_n \\\} \subset D
$$

Examples of elements include actors and actants in an actor domain,
processing units in a process domain, messages and signals in a communications
domain, or customers and sales orders in a business domain.

In general, there are no constraints on what an element can be—it depends
entirely on what you choose to model with presence assertions over $D$.
It is best to think of elements as playing the "thing" role in a presence
assertion. The same domain entity may appear in both element and boundary
roles.

Each element requires only a unique identifier, a user-facing name, and
optional metadata that can be used to filter or aggregate presences and
derived metrics.

This module contains the contract and implementations for an Element.
"""
from __future__ import annotations

import uuid
from typing import Protocol, runtime_checkable, Dict, Any, Optional


@runtime_checkable
class ElementProtocol(Protocol):
    """ The structural contract for an element """

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


class ElementMixin:
    """A mixin class that can be used to inject common shared behavior
    of elements.
    """

    def summary(self: ElementProtocol) -> str:
        """
        Return a human-readable summary based on id and metadata.
        """
        meta = getattr(self, "metadata", {})
        if not meta:
            return f"Element[{self.id}] name = {self.name} (no metadata)"
        formatted = ", ".join(f"{k}={v!r}" for k, v in meta.items())
        return f"Element[{self.id}] name = {self.name} {{{formatted}}}"


class ElementView(ElementMixin):
    """A view class that allows domain objects to behave like elements"""

    __slots__ = ("_id", "_name", "_metadata")

    def __init__(self, base: ElementProtocol):
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


class Element(ElementMixin, ElementProtocol):
    """A default implementation of fully functional element."""

    __slots__ = ("_id", "_name", "_metadata")

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
