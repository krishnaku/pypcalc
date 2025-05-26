# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from typing import Tuple
from .basis_topology import BasisTopology
from .presence import Presence


class PresenceInvariant:
    """
    Computes the components of the Presence Invariant directly from a BasisTopology.

    This invariant expresses a local conservation law of presence mass over any finite
    time interval [t0, t1), using only the closure of the topology.
    """

    def __init__(self, topology: BasisTopology):
        self.topology = topology
        self.closed_presences = topology.closure()

    def _filter_window(self, t0: float, t1: float) -> list[Presence]:
        return [
            p for p in self.closed_presences
            if p.overlaps(t0,t1)
        ]

    def get_presence_summary(self, t0: float, t1: float) -> Tuple[float, int, float]:
        """
        Computes:
        - Total presence mass A
        - Number of overlapping presences N
        - Interval length T
        """
        if t0 >= t1:
            return 0.0, 0, 0.0

        A = 0.0
        N = 0
        T = t1 - t0

        for p in self._filter_window(t0, t1):
            r = p.residence_time(t0, t1)
            if r > 0.0:
                A += r
                N += 1

        return A, N, T

    def avg_presence_density(self, t0: float, t1: float) -> float:
        A, _, T = self.get_presence_summary(t0, t1)
        return A / T if T > 0 else 0.0

    def incidence_rate(self, t0: float, t1: float) -> float:
        _, N, T = self.get_presence_summary(t0, t1)
        return N / T if T > 0 else 0.0


    def avg_presence_mass(self, t0: float, t1: float) -> float:
        A, N, _ = self.get_presence_summary(t0, t1)
        return A / N if N > 0 else 0.0

    def invariant(self, t0: float, t1: float) -> Tuple[float, float, float]:
        """
        Returns:
            (avg_presence_density, incidence_rate, avg_presence_mass)

        These satisfy the Presence Invariant:
            avg_presence_density = incidence_rate × avg_presence_mass
        """
        A, N, T = self.get_presence_summary(t0, t1)
        L = A / T if T > 0 else 0.0
        Λ = N / T if T > 0 else 0.0
        w = A / N if N > 0 else 0.0
        return L, Λ, w
