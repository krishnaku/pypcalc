# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy import typing as npt

"""
Presence matrices created from Boundary presences are Boolean: they indicate
whether or not an element was present in a boundary over a time interval. This is the base case 
for presence based flow analytics and represented by the type `BooleanPresence`. 

We may also apply functions to boolean presence matrix to transform it into a matrix
over the reals. In these cases, we will represent the resulting 
matrix using the type `RealPresence`.

The type variable `T_Matrix` represents the union of all possible matrix types. 
"""
BooleanPresence = npt.NDArray[np.int_]      # For binary matrices (0/1)
RealPresence = npt.NDArray[np.float64]  # For mapped/weighted matrices
PresenceMatrixType = BooleanPresence | RealPresence
T_Matrix = TypeVar("T_Matrix", BooleanPresence, RealPresence)


