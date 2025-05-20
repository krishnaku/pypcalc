# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from pcalc import Element, Boundary


class  MockElement(Element):
    def __init__(self, id='Mock Element'):
        self._id = id
        self._metadata = {}

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        return self._metadata

    def __str__(self) -> str:
        return self._id if self._id is not None else 'None'


class MockBoundary(Boundary):
    def __init__(self, id='Mock Boundary'):
        self._id = id
        self._metadata = {}

    @property
    def id(self):
        return self._id

    @property
    def metadata(self):
        return self._metadata

    def __str__(self) -> str:
        return self._id if self._id is not None else 'None'