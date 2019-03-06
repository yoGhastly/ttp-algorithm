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

# Calculate distance - pythagoras

distance_array = np.zeros(shape=[nodes.__len__(), nodes.__len__()])

for x in range(nodes.__len__()):
    distance_array[x] = np.power(np.power(nodes.transpose()[1] - nodes[x][1],2) + np.power(nodes.transpose()[2] - nodes[x][2],2),1/2)


# Generate random TSP solution

def generate_TSP_solution():
    index_pool = list(np.copy(index_array))
    route = np.empty(shape=index_array.__len__())
    for x in range (index_array.__len__()):
        node_index = random.choice(index_pool)
        route[x]=node_index
        index_pool.remove(node_index)
    return [route,0]  # returning [route, current KPN weight]


# Calculate velocity
def get_velocity(solution):
    return basic_info["max speed"] - solution[1]*(basic_info["max speed" ]- basic_info["min speed"]/basic_info["KNP cap"])

# Calculate time - f(x) function
def get_travel_time(start_index,destination_index,solution):
        return distance_array[start_index][destination_index]/get_velocity(solution)

