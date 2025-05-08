from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from typing import List, Optional

import numpy as np
from core import Signal

@dataclass
class Presence:
    """
    A continuous interval during which a signal is considered present within a boundary.

    A `Presence` captures a presence interval for a single `signal_id`, including start and end times,
    and internal metadata used to locate it within a `PresenceMatrix` row and time bins.

    A `core.boundary.Boundary` is responsible for mapping a set of point in time `core.signal_log.SignalEvents` into
    Presences.
    """

    signal: Signal
    """The signal this Presence corresponds to."""

    start: float
    """Start time of the Presence interval."""

    end: float
    """End time of the Presence interval."""

    presence_row: int = -1
    """The row index assigned to this Presence in the `PresenceMatrix`."""

    start_bin: int = -1
    """The index of the first time bin where the Presence is active."""

    end_bin: int = -1
    """The index of the last time bin where the Presence is active."""

    def overlaps(self, t0: int, t1: int) -> bool:
        """
        Check whether this Presence overlaps with the given time interval.

        Args:
            t0: Start of the comparison window.
            t1: End of the comparison window.

        Returns:
            True if the Presence overlaps any part of [t0, t1), False otherwise.
        """
        return self.start < t1 and self.end > t0

    def duration(self) -> float:
        """
        Return the duration of the Presence.

        Returns:
            The length of the interval in time units.
        """
        return self.end - self.start


class PresenceMatrix:
    """
    A time-binned matrix representation of signal presence across a boundary.

    Each row corresponds to a single `Presence`, and each column represents a time bin.
    The matrix is binary: a value of 1 indicates the signal was present in the boundary
    during that time bin, while 0 indicates absence.

    Note that the same signal may be present in a  given matrix multiple times, but they will
    be recorded as separate Presences and be represented as separate rows in the matrix.

    The `PresenceMatrix` is the core data structure used to analyze how signals
    propagate through boundaries over time, and to support calculations like frequency,
    dwell time, or signal overlap across entities or phases.

    ### Dimensions

    - Rows: `len(Presences)`
    - Columns: `(t1 - t0) / bin_width`

    ### Example

    ```python
    matrix = PresenceMatrix(Presences, t0=0.0, t1=10.0, bin_width=1.0)
    matrix.presence_matrix  # shape: (num_Presences, num_time_bins)
    ```
    """

    def __init__(self, presences: List[Presence], t0: float, t1: float, bin_width: float):
        """
        Construct a presence matrix from a list of Presences and time window configuration.

        Args:
            Presences: A list of `Presence` instances, one per signal of interest.
            t0: Start of the observation window.
            t1: End of the observation window.
            bin_width: Width of each time bin for discretization.
        """
        self.presences = presences
        self.t0 = t0
        self.t1 = t1
        self.bin_width = bin_width

        self.presence_matrix: Optional[np.ndarray] = None
        """The binary presence matrix with shape (num_Presences, num_bins)."""

        self.time_bins: int = 0
        """The number of bins used across the observation window."""

        self.init_matrix()

    def init_matrix(self):
        """
        Initialize the internal binary presence matrix based on the Presence intervals and binning scheme.
        """
        presences = self.presences
        t0 = self.t0
        t1 = self.t1
        bin_width = self.bin_width

        time_bins = np.arange(t0, t1 + bin_width, bin_width)
        num_bins = len(time_bins) - 1
        num_rows = len(presences)

        # we use float here because a presence matrix in general can be
        # transformed by arbitrary presence functions.
        presence = np.zeros((num_rows, num_bins), dtype=float)

        for i, presence in enumerate(presences):
            presence.presence_row = i

            # Clip presence interval to the time window
            effective_start = max(presence.start, t0)
            effective_end = min(presence.end, t1)

            # Convert to bin indices
            start_bin = int((effective_start - t0) // bin_width)
            end_bin = int((effective_end - t0) // bin_width)

            if end_bin > start_bin:
                presence[i, start_bin:end_bin] = 1

            presence.start_bin = start_bin
            presence.end_bin = end_bin

        self.presence_matrix = presence
        self.time_bins = time_bins


