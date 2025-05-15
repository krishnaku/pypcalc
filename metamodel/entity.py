# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from typing import Protocol, Dict, Any

from typing import Protocol, Dict, Any
from .element import Element


class Entity(Element, Protocol):
    """
    An `Entity` is any named element in the domain.

    This protocol defines the minimal interface required for an object to be treated as an entity:
    a stable identifier (as an element), a human-readable name, and optional metadata.

    This abstraction is useful for modeling agents, nodes, resources, boundaries. devices, constraints
    or participants in a networked or simulated domain.

    ### Example

    ```python
    class User(Entity):
        def __init__(self, user_id: str, name: str):
            self._id = user_id
            self._name = name

        @property
        def id(self) -> str:
            return self._id

        @property
        def name(self) -> str:
            return self._name

        @property
        def metadata(self) -> Dict[str, Any]:
            return {"role": "user"}
    ```
    """

    @property
    def name(self) -> str:
        """A human-readable name for display or debugging."""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """Optional key-value metadata associated with the entity."""
        ...
