# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import uuid
from typing import Protocol, runtime_checkable, Dict, Any, Optional


# ----------------------------------------
# Protocol: structural contract
# ----------------------------------------

@runtime_checkable
class ElementProtocol(Protocol):
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


# ----------------------------------------
# Mixin: shared logic for any compatible class
# ----------------------------------------

class ElementMixin:
    def summary(self: ElementProtocol) -> str:
        """
        Return a human-readable summary based on id and metadata.
        """
        meta = getattr(self, "metadata", {})
        if not meta:
            return f"Element[{self.id}] name = {self.name} (no metadata)"
        formatted = ", ".join(f"{k}={v!r}" for k, v in meta.items())
        return f"Element[{self.id}] name = {self.name} {{{formatted}}}"


# ----------------------------------------
# View: wrap arbitrary duck-typed objects
# ----------------------------------------

class ElementView(ElementMixin):
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


# ----------------------------------------
# Default implementation
# ----------------------------------------
class Element(ElementMixin, ElementProtocol):

    def __init__(self, id: Optional[str] = None, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        self._id: str = id or str(uuid.uuid4())
        self._name: str = name or self.id
        self._metadata: Dict[str,Any] = metadata or {}

    @property
    def id(self) -> str:
        return self._id

    # noinspection PyProtocol
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name:str) -> None:
        self._name = name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def __str__(self) -> str:
        return self.summary()