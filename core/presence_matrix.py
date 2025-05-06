from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from boundary import Boundary  # Only for static type checkers

from collections import defaultdict
from typing import Dict, List, Optional

import numpy as np
from core import SignalEvent

@dataclass
class Visit:
    signal_id: str
    start: float
    end: float
    presence_row: int = -1
    start_bin: int = -1
    end_bin: int = -1

    def overlaps(self, t0: int, t1: int) -> bool:
        return self.start < t1 and self.end > t0

    def duration(self) -> float:
        return self.end - self.start


class PresenceMatrix:
    def __init__(self, visits: List[Visit], t0: float, t1: float, bin_width: float):
        self.visits = visits
        self.t0 = t0
        self.t1 = t1
        self.bin_width = bin_width

        self.presence_matrix: Optional[np.ndarray] = None
        self.time_bins: int = 0


        self.init_matrix()

    def init_matrix(self):
        visits = self.visits
        t0 = self.t0
        t1 = self.t1
        bin_width = self.bin_width

        time_bins = np.arange(t0, t1 + bin_width, bin_width)
        num_bins = len(time_bins) - 1
        num_rows = len(visits)
        # Initialize presence matrix
        presence = np.zeros((num_rows, num_bins), dtype=int)
        for i, visit in enumerate(visits):
            visit.presence_row = i

            # Clip start and end to t0 and t1 bounds
            effective_start = max(visit.start, t0)
            effective_end = min(visit.end, t1)

            # Convert to bin indices
            start_bin = int((effective_start - t0) // bin_width)
            end_bin = int((effective_end - t0) // bin_width)

            # Clamp to matrix bounds
            if end_bin > start_bin:
                presence[i, start_bin:end_bin] = 1
            visit.start_bin = start_bin
            visit.end_bin = end_bin

            # Fill presence matrix and update visit metadata
            presence[i, start_bin:end_bin] = 1
            visit.start_bin = start_bin
            visit.end_bin = end_bin

        self.presence_matrix = presence
        self.time_bins = time_bins


