from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from typing import List, Optional

import numpy as np
from core import Signal

@dataclass
class Visit:
    """
    A continuous interval during which a signal is considered present within a boundary.

    A `Visit` captures a presence interval for a single `signal_id`, including start and end times,
    and internal metadata used to locate it within a `PresenceMatrix` row and time bins.

    A `core.boundary.Boundary` is responsible for mapping a set of point in time `core.signal_log.SignalEvents` into
    Visits.
    """

    signal: Signal
    """The signal this visit corresponds to."""

    start: float
    """Start time of the visit interval."""

    end: float
    """End time of the visit interval."""

    presence_row: int = -1
    """The row index assigned to this visit in the `PresenceMatrix`."""

    start_bin: int = -1
    """The index of the first time bin where the visit is active."""

    end_bin: int = -1
    """The index of the last time bin where the visit is active."""

    def overlaps(self, t0: int, t1: int) -> bool:
        """
        Check whether this visit overlaps with the given time interval.

        Args:
            t0: Start of the comparison window.
            t1: End of the comparison window.

        Returns:
            True if the visit overlaps any part of [t0, t1), False otherwise.
        """
        return self.start < t1 and self.end > t0

    def duration(self) -> float:
        """
        Return the duration of the visit.

        Returns:
            The length of the interval in time units.
        """
        return self.end - self.start


class PresenceMatrix:
    """
    A time-binned matrix representation of signal presence across a boundary.

    Each row corresponds to a single `Visit`, and each column represents a time bin.
    The matrix is binary: a value of 1 indicates the signal was present in the boundary
    during that time bin, while 0 indicates absence.

    Note that the same signal may be present in a  given matrix multiple times, but they will
    be recorded as separate visits and be represented as separate rows in the matrix.

    The `PresenceMatrix` is the core data structure used to analyze how signals
    propagate through boundaries over time, and to support calculations like frequency,
    dwell time, or signal overlap across entities or phases.

    ### Dimensions

    - Rows: `len(visits)`
    - Columns: `(t1 - t0) / bin_width`

    ### Example

    ```python
    matrix = PresenceMatrix(visits, t0=0.0, t1=10.0, bin_width=1.0)
    matrix.presence_matrix  # shape: (num_visits, num_time_bins)
    ```
    """

    def __init__(self, visits: List[Visit], t0: float, t1: float, bin_width: float):
        """
        Construct a presence matrix from a list of visits and time window configuration.

        Args:
            visits: A list of `Visit` instances, one per signal of interest.
            t0: Start of the observation window.
            t1: End of the observation window.
            bin_width: Width of each time bin for discretization.
        """
        self.visits = visits
        self.t0 = t0
        self.t1 = t1
        self.bin_width = bin_width

        self.presence_matrix: Optional[np.ndarray] = None
        """The binary presence matrix with shape (num_visits, num_bins)."""

        self.time_bins: int = 0
        """The number of bins used across the observation window."""

        self.init_matrix()

    def init_matrix(self):
        """
        Initialize the internal binary presence matrix based on the visit intervals and binning scheme.
        """
        visits = self.visits
        t0 = self.t0
        t1 = self.t1
        bin_width = self.bin_width

        time_bins = np.arange(t0, t1 + bin_width, bin_width)
        num_bins = len(time_bins) - 1
        num_rows = len(visits)

        presence = np.zeros((num_rows, num_bins), dtype=int)

        for i, visit in enumerate(visits):
            visit.presence_row = i

            # Clip visit interval to the time window
            effective_start = max(visit.start, t0)
            effective_end = min(visit.end, t1)

            # Convert to bin indices
            start_bin = int((effective_start - t0) // bin_width)
            end_bin = int((effective_end - t0) // bin_width)

            if end_bin > start_bin:
                presence[i, start_bin:end_bin] = 1

            visit.start_bin = start_bin
            visit.end_bin = end_bin

        self.presence_matrix = presence
        self.time_bins = time_bins


