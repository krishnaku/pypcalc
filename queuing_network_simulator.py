import simpy
import numpy as np
import uuid
import networkx as nx
from typing import Dict

from signal_history import SignalHistory


class QueuingNetworkSimulation:
    def __init__(self, env, network: nx.DiGraph, simulation_period, seed=42):
        self.env = env
        self.network = network
        self.queues = {node: simpy.Resource(env, capacity=network.nodes[node].get("concurrency", 1)) for node in
                       network.nodes}
        self.delay_map = {node: network.nodes[node].get("delay", 1.0) for node in network.nodes}
        self.queue_signal_history: Dict[str, SignalHistory] = {node: SignalHistory(node, simulation_period) for node in network.nodes}
        self.system_signal_history = SignalHistory("System", simulation_period)
        self.entity_system_state = {}
        self.rng = np.random.default_rng(seed)

    def signal_enter(self, node: str, entity_id: str):
        t_enter = self.env.now
        self.queue_signal_history[node].add("enter", t_enter, entity_id)
        state = self.entity_system_state[entity_id]
        if not state["entered"]:
            self.system_signal_history.add("enter", t_enter, entity_id)
            state["entered"] = True

        return t_enter

    def signal_start_service(self, node: str, entity_id: str):
        t_start = self.env.now
        self.queue_signal_history[node].add("start_service", t_start, entity_id)
        return t_start

    def signal_end_service(self, node: str, entity_id: str):
        t_end = self.env.now
        self.queue_signal_history[node].add("end_service", t_end, entity_id)
        return t_end

    def signal_exit(self, node: str, entity_id: str):
        t_exit = self.env.now
        self.queue_signal_history[node].add("exit", t_exit, entity_id)
        state = self.entity_system_state[entity_id]
        if self.network.out_degree(node) == 0 and not state["exited"]:
            self.system_signal_history.add("exit", t_exit, entity_id)
            state["exited"] = True
        return t_exit

    def entity(self, start_node="A"):
        entity_id = str(uuid.uuid4())
        current_node = start_node
        self.entity_system_state.setdefault(entity_id, {"entered": False, "exited": False})
        while current_node is not None:
            self.signal_enter(current_node, entity_id)
            yield from self.service(current_node, entity_id)
            self.signal_exit(current_node, entity_id)
            # Determine next node from transition probabilities
            current_node = self.get_next_node(current_node)

    def get_next_node(self, current_node):
        if self.network.out_degree(current_node) > 0:
            edges = list(self.network.out_edges(current_node, data=True))
            probs = [e[2].get("prob", 1.0) for e in edges]
            next_nodes = [e[1] for e in edges]
            total = sum(probs)
            probs = [p / total for p in probs]
            next_node = self.rng.choice(next_nodes, p=probs)
            return next_node

        return None

    def service(self, current_node, entity_id):
        if self.network.nodes[current_node].get("concurrency") is not None:
            with self.queues[current_node].request() as req:
                yield req
        # if there are no concurrency limits the service has infinite concurrency
        # ie it is a pure delay.
        self.signal_start_service(current_node, entity_id)
        yield from self.service_process(current_node)
        self.signal_end_service(current_node, entity_id)

    def service_process(self, current_node):
        delay = self.delay_map[current_node]
        yield self.env.timeout(delay)

    def arrival_process(self, arrival_rate, start_node="A", T=100):
        while self.env.now < T:
            if self.rng.random() < arrival_rate:
                self.env.process(self.entity(start_node))
            yield self.env.timeout(1)


class SimulationResult:
    def __init__(self, queue_signal_history: Dict[str, SignalHistory], system_signal_history: SignalHistory, T: int):
        self.queue_signal_history = queue_signal_history
        self.system_signal_history = system_signal_history
        self.T = T

    def get_signal_history(self, node: str) -> SignalHistory:
        return self.queue_signal_history[node]

    def get_system_signal_history(self) -> SignalHistory:
        return self.system_signal_history


def run_simulation(network: nx.DiGraph, T=100, arrival_rate=0.1, seed=42,
                   start_node="A") -> SimulationResult:
    env = simpy.Environment()
    simulation_run = QueuingNetworkSimulation(env, network, T, seed=seed)
    env.process(simulation_run.arrival_process(arrival_rate, start_node=start_node, T=T))
    env.run(until=T)
    return SimulationResult(simulation_run.queue_signal_history, simulation_run.system_signal_history, T)
