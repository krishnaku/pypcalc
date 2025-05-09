# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
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
