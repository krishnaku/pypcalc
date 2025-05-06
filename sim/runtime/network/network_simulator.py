# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved
# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.
# Author: Krishna Kumar


import logging
from typing import Dict, Any

import networkx as nx

from sim.model.collaborator import CollaboratorBase, collaborator_registry
from sim.runtime.simulation import Simulation
from misc.collection_utils import without_keys

log = logging.getLogger(__name__)

class NetworkSimulation(Simulation):
    def __init__(
            self,
            network: nx.DiGraph,
            runs=1,
            until=20,
            realtime_factor=None):
        # init the simulation parameters and model
        super().__init__(
            until,
            runs,
            realtime_factor
        )
        self.network: nx.DiGraph = network
        self.config: Dict[str, Dict[str, Any]] = {}
        self.collaborators: Dict[str, CollaboratorBase] = {}

    def load_node_config(self, node: str, defaults: dict[str, Any] = None) -> dict[str, Any]:
        config = dict(self.network.nodes[node])
        if defaults:
            for k, v in defaults.items():
                config.setdefault(k, v)
        return config

    def init_peers(self):
        for node in self.network.nodes:
            config = self.config[node]
            if 'peer' in config:
                this = self.collaborators[node]
                peer = self.collaborators.get(config['peer'])
                if peer is not None:
                    if this.peer is None and peer.peer is None:
                        this.set_peer(peer)

    def int_collaborators(self):
        for node in self.network.nodes:
            config = self.load_node_config(node)
            self.config[node] = config

            if 'kind' in config:
                self.collaborators[node] = collaborator_registry.create(sim_context=self, **config)
            else:
                raise ValueError(f"Collaborator {node} must specify 'kind' in config ")

    def bind_environment(self):
        self.int_collaborators()
        # temporary fix: wire up peer from attributes. This needs more refinement.
        self.init_peers()

    def start_processes(self):
        for collaborator in self.collaborators.values():
            collaborator.start_processes()

    def post_run(self):
        super().post_run()


# --- Example Usage ---

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    G = nx.DiGraph()
    G.add_node("A", name="A", kind="Requestor", delay_behavior=dict(kind="Markov", mean_time_between_requests=2))
    G.add_node("B", name="B", kind="Responder", peer="A",  delay_behavior=dict(kind="Markov", avg_processing_time=1.5))

    sim=NetworkSimulation(G)

    sim.run(until=10, runs=1)

    print(sim.latest_log.display())