# Auto-generated module

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uuid
from collections import deque

def run_simulation(T=200, arrival_rate=0.8, service_delay_A=2, service_delay_B=2, service_delay_C=2, rework_prob=0.2, seed=42):
    np.random.seed(seed)
    estimated_arrivals = int(arrival_rate * T * 1.5)
    queues = ['A', 'B', 'C', 'System']
    presence = {q: np.zeros((estimated_arrivals, T), dtype=bool) for q in queues}
    arrival_index = {q: np.zeros(T, dtype=int) for q in queues}
    visit_index = {q: [[] for _ in range(estimated_arrivals)] for q in queues}
    entity_index = {}
    queue_A, queue_B, queue_C = (deque(), deque(), deque())
    entity_counter = 0

    def process_queue(queue, service_delay, current_time, next_queue):
        new_queue = deque()
        for item in queue:
            if current_time - item['start_time'] >= service_delay:
                if next_queue is not None:
                    item['start_time'] = current_time
                    next_queue.append(item)
            else:
                new_queue.append(item)
        return new_queue

    def record_presence(queue_id, item, t, entity_index, presence, arrival_index):
        row = entity_index[item['id']]
        presence[queue_id][row, t] = True
        if t == 0 or not presence[queue_id][row, t - 1]:
            arrival_index[queue_id][t] += 1
            visit_index[queue_id][row].append(t)
    for t in range(T):
        if np.random.rand() < arrival_rate:
            entity_id = str(uuid.uuid4())
            entity_index[entity_id] = entity_counter
            queue_A.append({'id': entity_id, 'start_time': t})
            entity_counter += 1
        new_C = deque()
        for item in queue_C:
            if t - item['start_time'] >= service_delay_C:
                if np.random.rand() < rework_prob:
                    item['start_time'] = t
                    queue_A.append(item)
            else:
                new_C.append(item)
        queue_C = new_C
        queue_B = process_queue(queue_B, service_delay_B, t, queue_C)
        queue_A = process_queue(queue_A, service_delay_A, t, queue_B)
        for queue_id, queue in zip(['A', 'B', 'C'], [queue_A, queue_B, queue_C]):
            for item in queue:
                record_presence(queue_id, item, t, entity_index, presence, arrival_index)
                record_presence('System', item, t, entity_index, presence, arrival_index)
    return (presence, arrival_index, entity_index, visit_index)

