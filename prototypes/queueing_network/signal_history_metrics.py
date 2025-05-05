# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

class SignalHistoryMetric(ABC):
    @abstractmethod
    def update(self, signal_type: str, timestamp: float, signal_id: str):
        pass

    @abstractmethod
    def get_time_series(self):
        pass

    @abstractmethod
    def get_current_value(self):
        pass

    @abstractmethod
    def plot(self, ax=None, **kwargs):
        pass


class QueueLength(SignalHistoryMetric):
    def __init__(self, name, measurement_window: int):
        self.name = name
        self.measurement_window = measurement_window
        self.L = np.zeros(measurement_window, dtype=int)
        self._current_L = 0
        self._last_t = 0

    def get_time_series(self):
        return self.L

    def get_current_value(self):
        return self._current_L

    def update(self, signal_type: str, timestamp: float, signal_id: str=None):
        t = int(timestamp)

        # Fill in L from last_t to t
        end = min(t, self.measurement_window)
        self.L[self._last_t:end] = self._current_L

        if signal_type == "enter":
            self._current_L += 1
        elif signal_type == "exit":
            self._current_L -= 1

        if t < self.measurement_window:
            self.L[t] = self._current_L

        self._last_t = min(t + 1, self.measurement_window)

    def plot(self, ax=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        time_axis = range(self.measurement_window)
        label = "Queue Length"

        ax.plot(time_axis, self.L, label=label, **kwargs)

        avg_L = float(np.mean(self.L))
        ax.axhline(y=avg_L, color='gray', linestyle='--', linewidth=1, label=f"Avg = {avg_L:.2f}")
        ax.set_xlabel("Time")
        ax.set_ylabel("L(t)")

        title = f"{self.name}: Queue Length Over Time"
        ax.set_title(title)
        ax.legend()
        return ax