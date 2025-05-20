# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import uuid
from typing import Dict, Any, Optional

from sim.metamodel import Entity
from sim.runtime.simulation import Simulation

class EntityBase(Entity):
    """Base for a concrete domain component."""
    def __init__(self, name, domain_context: Simulation, id:Optional[str]=None, **kwargs) -> None:
        self._id: str =str(uuid.uuid4()) if id is None else id
        self._name: str = name
        self._domain_context: Simulation = domain_context
        self._metadata: Optional[Dict[str, Any]] = kwargs

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    @property
    def domain_context(self) -> Simulation:
        return self._domain_context