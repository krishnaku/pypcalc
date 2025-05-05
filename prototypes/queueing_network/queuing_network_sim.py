import simpy
import uuid
import networkx as nx
from typing import Dict
from core.simulation_context import SimulationContext
from prototypes.queueing_network.signal_history import SignalHistory
from prototypes.queueing_network.base_node import Node
from prototypes.queueing_network.network_node import NetworkNode, node_registry


class QueuingNetworkSimulation(SimulationContext):
    def __init__(self, env, network: nx.DiGraph, simulation_period, seed=42):
        super().__init__(env, seed)
        self._network = network

        self.queue_signal_history: Dict[str, SignalHistory] = {node: SignalHistory(node, simulation_period) for node in network.nodes}
        self.system_signal_history = SignalHistory("System", simulation_period)
        self.entity_system_state = {}

        self.nodes: Dict[str, NetworkNode] = {}

    def initialize_nodes(self):
        for name in self._network.nodes:
            config = self._network.nodes[name]
            node_type = config.get("type")
            if node_type is None:
                raise ValueError(f"Node {name} has no type defined")
            self.nodes[name] = node_registry.create(
                node_type,
                name=name,
                graph=self._network,
                sim_context=self
            )



    @property
    def network(self):
        return self._network



    def get_node(self, name: str) -> Node:
        return self.nodes[name]

    def signal_enter(self, node: str, signal_id: str):
        t_enter = self.env.now
        self.queue_signal_history[node].add(source=self.get_node(node), signal_type="enter", timestamp=t_enter, signal_id=signal_id)
        state = self.entity_system_state[signal_id]
        if not state["entered"]:
            self.system_signal_history.add("enter", t_enter, signal_id)
            state["entered"] = True

        return t_enter

    def signal_start_service(self, node: str, signal_id: str):
        t_start = self.env.now
        self.queue_signal_history[node].add("start_service", t_start, signal_id)
        return t_start

    def signal_end_service(self, node: str, signal_id: str):
        t_end = self.env.now
        self.queue_signal_history[node].add("end_service", t_end, signal_id)
        return t_end

    def signal_exit(self, node: str, signal_id: str):
        t_exit = self.env.now
        self.queue_signal_history[node].add("exit", t_exit, signal_id)
        state = self.entity_system_state[signal_id]
        if self.network.out_degree(node) == 0 and not state["exited"]:
            self.system_signal_history.add("exit", t_exit, signal_id)
            state["exited"] = True
        return t_exit

    def entity(self, start_node="A"):
        signal_id = str(uuid.uuid4())
        current = start_node
        self.entity_system_state.setdefault(signal_id, {"entered": False, "exited": False})
        while current is not None:
            current_node = self.nodes[current]
            self.signal_enter(current, signal_id)

            yield from current_node.service(signal_id)

            self.signal_exit(current, signal_id)
            current = current_node.choose_next_node(signal_id)

    def arrival_process(self, arrival_rate, start_node=None, T=100):
        if start_node is None:
            raise ValueError("Start node must be specified")

        while self.env.now < T:
            self.env.process(self.entity(start_node))
            yield self.env.timeout(1/arrival_rate)



class SimulationResult:
    def __init__(self, queue_signal_history: Dict[str, SignalHistory], system_signal_history: SignalHistory, T: int):
        self.queue_signal_history = queue_signal_history
        self.system_signal_history = system_signal_history
        self.T = T

    def get_signal_history(self, node: str) -> SignalHistory:
        return self.queue_signal_history[node]

    def get_system_signal_history(self) -> SignalHistory:
        return self.system_signal_history


def run_simulation(network: nx.DiGraph, start_node=None,  T=100, arrival_rate=0.1, seed=42) -> SimulationResult:
    env = simpy.Environment()
    simulation_run = QueuingNetworkSimulation(env, network, simulation_period=T,   seed=seed)
    env.process(simulation_run.arrival_process(arrival_rate, start_node=start_node, T=T))
    env.run(until=T)
    return SimulationResult(simulation_run.queue_signal_history, simulation_run.system_signal_history, T)
