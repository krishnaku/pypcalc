# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


from typing import Protocol, TypeVar, Dict, Any

T_Element = TypeVar('T_Element', bound='Element')

class Element(Protocol):
    """Identifiable members of a domain."""

    @property
    def id(self) -> str:
        """A stable unique identifier for the element (used for indexing and lookup)."""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """Optional key-value metadata associated with the element."""
        ...
