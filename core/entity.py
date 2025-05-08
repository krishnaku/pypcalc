# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Protocol, Dict, Any

""""""
from typing import Protocol, Dict, Any

class Entity(Protocol):
    """
    Marker protocol for actants in the domain.

    An `Entity` is any named participant in a domain that can emit or receive signals.
    This protocol defines the minimal interface required for an object to be treated as an entity:
    a stable identifier, a human-readable name, and optional metadata.

    This abstraction is useful for modeling agents, nodes, resources, devices, constraints or participants in a networked or simulated domain.

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
