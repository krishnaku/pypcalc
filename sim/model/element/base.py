# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import uuid

from metamodel import Element


class ElementBase(Element):
    # Element implementation
    def __init__(self, id=None):
        self._id = str(uuid.uuid4()) if id is None else id

    @property
    def id(self) -> str:
        """The unique ID of the signal (auto-assigned)."""
        return self._id
