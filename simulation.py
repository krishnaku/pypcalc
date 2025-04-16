from abc import abstractmethod

import simpy
import numpy as np
from base_node import Boundary


class Simulation:
    def __init__(self, env: simpy.Environment, seed: int) -> None:
        self._env = env
        self._rng = np.random.default_rng(seed)

    @property
    def env(self):
        return self._env

    @property
    def rng(self):
        return self._rng

    @abstractmethod
    def get_node(self, name: str) -> Boundary:
        pass