import random

import loader
import pandas as pd
import numpy as np

# Data import

basic_info, nodes, items = loader.load('easy_0.ttp')

# Gathering index

index_array = np.zeros(shape=nodes.__len__(), dtype=int)
for x in range(nodes.__len__()):
    index_array[x] = (nodes[x][0])

# Calculate distance - atm I'm assuming that we can move only on edges |xi - xj| + |yi - yj|

distance_array = np.zeros(shape=[nodes.__len__(), nodes.__len__()])

for x in range(nodes.__len__()):
    distance_array[x] = np.abs(nodes.transpose()[1] - nodes[x][1]) + np.abs(nodes.transpose()[2] - nodes[x][2])


# Generate random TSP solution

def generate_TSP_solution():
    index_pool = list(np.copy(index_array))
    solution = np.empty(shape=index_array.__len__())
    for x in range (index_array.__len__()):
        node_index = random.choice(index_pool)
        solution[x]=node_index
        index_pool.remove(node_index)
    return solution


