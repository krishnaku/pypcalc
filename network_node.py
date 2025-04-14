# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Set
from xml.dom import ValidationErr

import networkx as nx
import simpy

class NetworkNode(ABC):
    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name: str = name
        self.config: Dict[str, Any] = config

    @abstractmethod
    def request_service(self, entity_id: str) -> Any:
        """Yield if blocking (e.g. wait for resource)."""
        pass

    @abstractmethod
    def perform_service(self, entity_id: str) -> Any:
        """Actual service duration once started."""
        pass

    @abstractmethod
    def choose_next_node(self, entity: Any) -> Optional[str]:
        pass


class NetworkXNode(NetworkNode, ABC):
    def __init__(self, name: str, graph: nx.DiGraph, exit_nodes: Set[str]=None) -> None:
        config: Dict[str, Any] = graph.nodes[name]
        super().__init__(name, config)
        self.graph: nx.DiGraph = graph



class DefaultNode(NetworkXNode):
    def __init__(self, name: str, graph: nx.DiGraph, env, rng ):
        super().__init__(name, graph)
        self.env = env
        self.rng = rng
        self.delay = self.config.get("delay", 1.0)
        self._init_concurrency(env)
        self._init_probabilities(graph)

    def _init_concurrency(self, env):
        self.concurrency = self.config.get("concurrency")
        if self.concurrency:
            self.resource = simpy.Resource(env, capacity=self.concurrency)
        else:
            self.resource = None

    def _init_probabilities(self, graph):
        self.next_nodes = []
        self.probs = []
        neighbors = list(self.graph.out_edges(self.name, data=True))
        if len(neighbors) > 0:
            self.next_nodes = [e[1] for e in neighbors]
            self.probs = [e[2].get("prob", 1.0) for e in neighbors]
            if self.next_nodes and abs(sum(self.probs) - 1.0) > 1e-6:
                raise ValueError(f"The probabilities on outgoing edges on node {self.name} do not sum to 1.")


    def choose_next_node(self, entity) -> Optional[str]:
        if not self.next_nodes:
            return None
        return self.rng.choice(self.next_nodes, p=self.probs)



    def request_service(self, entity_id: str):
        if self.concurrency:
            with self.resource.request() as req:
                yield req
        else:
            return

    def perform_service(self, entity_id: str):
        yield self.env.timeout(self.delay)

