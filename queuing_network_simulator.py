import simpy
import numpy as np
import uuid
import networkx as nx
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Signal:
    timestamp: float
    entity_id: str
    signal_type: str  # 'enter', 'exit', optionally 'start_service'


class SignalHistory:
    def __init__(self):
        self.signals: List[Signal] = []

    def add(self, signal_type: str, timestamp: float, entity_id: str):
        self.signals.append(Signal(timestamp, entity_id, signal_type))

    def get_signals(self, signal_type: str = None) -> List[Signal]:
        if signal_type:
            return [s for s in self.signals if s.signal_type == signal_type]
        return self.signals

    def sort(self):
        self.signals.sort(key=lambda s: s.timestamp)

    def __str__(self):
        if not self.signals:
            return "SignalHistory: (no signals)"

        from collections import Counter

        types = Counter(s.signal_type for s in self.signals)
        times = [s.timestamp for s in self.signals]
        entities = set(s.entity_id for s in self.signals)

        summary = [
            f"SignalHistory ({len(self.signals)} signals)",
            f"  Types: " + ", ".join(f"{t}={n}" for t, n in types.items()),
            f"  Time range: {min(times):.2f} to {max(times):.2f}",
            f"  Unique entities: {len(entities)}",
        ]
        return "\n".join(summary)


class GraphQueueSystem:
    def __init__(self, env, graph: nx.DiGraph, seed=42):
        self.env = env
        self.graph = graph
        self.queues = {node: simpy.Resource(env, capacity=graph.nodes[node].get("concurrency", 1)) for node in
                       graph.nodes}
        self.delay_map = {node: graph.nodes[node].get("delay", 1.0) for node in graph.nodes}
        self.queue_signal_history: Dict[str, SignalHistory] = {node: SignalHistory() for node in graph.nodes}
        self.system_signal_history = SignalHistory()
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
        if self.graph.out_degree(node) == 0 and not state["exited"]:
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
        if self.graph.out_degree(current_node) > 0:
            edges = list(self.graph.out_edges(current_node, data=True))
            probs = [e[2].get("prob", 1.0) for e in edges]
            next_nodes = [e[1] for e in edges]
            total = sum(probs)
            probs = [p / total for p in probs]
            next_node = self.rng.choice(next_nodes, p=probs)
            return next_node

        return None

    def service(self, current_node, entity_id):
        if self.graph.nodes[current_node].get("concurrency") is not None:
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


def run_graph_simulation(graph: nx.DiGraph, T=100, arrival_rate=0.1, concurrency=1, seed=42,
                         start_node="A") -> SimulationResult:
    env = simpy.Environment()
    system = GraphQueueSystem(env, graph, concurrency=concurrency, seed=seed)
    env.process(system.arrival_process(arrival_rate, start_node=start_node, T=T))
    env.run(until=T)
    return SimulationResult(system.queue_signal_history, system.system_signal_history, T)
