# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Any, Optional, Dict, Generator
import networkx as nx

from sim.model.registry import Registry
from prototypes.queueing_network.base_node import Node
from metamodel.boundary import Boundary
from prototypes.queueing_network.routing import RoutingMixin, router_registry
from metamodel.domain import DomainContext

from prototypes.queueing_network.delay_node import BlockingDelay, PureDelay


class NetworkNode(RoutingMixin, Node):
    def __init__(self, name: str, graph: nx.DiGraph, sim_context: DomainContext) -> None:
        config: Dict[str, Any] = graph.nodes[name]
        super().__init__(name, config, sim_context)
        self.graph: nx.DiGraph = graph
        self.setup_routing(config, node=self)

    def route(self, signal_id: str, **kwargs) -> Optional[Boundary]:
        next_name = self.routing_fn(signal_id=signal_id, node=self, **kwargs)
        return self.sim_context.get_node(next_name)

    def on_exit(self, signal_id: str, **kwargs) -> Generator:
        next_node = self.route(signal_id, **kwargs)
        if next_node is None:
            return
        yield from next_node.enter(signal_id, **kwargs)






# A registry for network node objects
node_registry: Registry[NetworkNode] = Registry()

@node_registry.register("pure_delay")
class NPureDelay(PureDelay, NetworkNode):
    def __init__(self, name: str, graph: nx.DiGraph, sim_context: DomainContext) -> None:
        config = graph.nodes[name]
        PureDelay.__init__(self, name, config, sim_context)
        NetworkNode.__init__(self, name, graph, sim_context)

@node_registry.register("blocking_delay")
class NBlockingDelay(BlockingDelay, NetworkNode):
    def __init__(self, name: str, graph: nx.DiGraph, sim_context: DomainContext) -> None:
        config = graph.nodes[name]
        BlockingDelay.__init__(self, name, config, sim_context)
        NetworkNode.__init__(self, name, graph, sim_context)

@router_registry.register("probabilistic")
class ProbabilisticRouter:
    def __init__(self, node: NetworkNode, **params) -> None:
        self.node = node
        self.rng = None
        self.next_nodes = []
        self.probs = []
        self.initialize(**params)

    def initialize(self, **params) -> None:
        # Access sim_context’s rng
        self.rng = self.node.sim_context.rng

        edges = list(self.node.graph.out_edges(self.node.name, data=True))
        self.next_nodes = [tgt for _, tgt, _ in edges]
        self.probs = [data.get("prob", 1.0) for _, _, data in edges]
        if abs(sum(self.probs) - 1.0) > 1e-6:
            raise ValueError(f"Probabilities at {self.node.name} don't sum to 1.")

    def __call__(self, signal_id: str, node: NetworkNode, **kwargs) -> Optional[str]:
        if not self.next_nodes:
            return None
        return self.rng.choice(self.next_nodes, p=self.probs)





