import random
import loader
import numpy as np
import pandas as pd
from operator import itemgetter
import time
start_time = time.time()

np.set_printoptions(threshold=np.nan)


# Data import

basic_info, nodes, items = loader.load('medium_1.ttp')

KNP_greedy_strategies = ['most_expensive','lightest','best_ratio']  #ratio = profit/weight

#Calculate max amount of items
def max_amount_items():
    return np.max(np.bincount(items.transpose()[3]))

# Assign items to cities

# city_item_list[city_index - 1] = list of items for city with city_index      /each item is stored as a list [index,profit,weight]

city_item_list = [None] * len(items)

for x in range (len(items)):
    if(city_item_list[items[x][3] -1] is None):
        city_item_list[items[x][3] - 1] = [list(items[x][:3])]
    else:
        city_item_list[(items[x][3] - 1)].append(list(items[x][:3]))


# Gathering index

index_array = np.zeros(shape=nodes.__len__(), dtype=int)
for x in range(nodes.__len__()):
    index_array[x] = (nodes[x][0])

# Calculate distance - pythagoras

distance_array = np.zeros(shape=[nodes.__len__(), nodes.__len__()])
for x in range(nodes.__len__()):
    distance_array[x] = np.power(np.power(nodes.transpose()[1] - nodes[x][1],2) + np.power(nodes.transpose()[2] - nodes[x][2],2),1/2)

def get_Matrix():
    return distance_array

# Generate random TSP solution

def generate_TSP_solution():
    index_pool = list(np.copy(index_array))
    route = np.empty(shape=index_array.__len__())

    for x in range (index_array.__len__()):
        node_index = random.choice(index_pool)
        route[x] = node_index
        index_pool.remove(node_index)
    return route  # returning [route]


# Calculate velocity
def get_velocity(current_cap):
    return basic_info["max speed"] - current_cap*((basic_info["max speed" ]- basic_info["min speed"])/basic_info["KNP cap"])

# Calculate time - f(x) function
def get_travel_time(start_index,destination_index,curr_cap):
        return distance_array[start_index][destination_index]/get_velocity(curr_cap)


# Get all items for a city
def get_items_for_city(index):
    """:rtype: list"""
    result = city_item_list[index-1]
    return result

# Get list of all items:
def get_all_items():
    return items[:, [0, 1, 2]].tolist()

# Get item - use this function if u assume that u're trying to pick up items every time we visit a city

def get_item(city_index,strategy,current_cap):
    picked_item = None
    city_items = []
    if(strategy == 'most_expensive'):
        city_items = sorted(city_item_list[city_index - 1].copy(),key=itemgetter(1),reverse=True)                       # copy array and sort items by profit

    # - HAVEN'T TESTED IT YET
    elif(strategy=='lightest'):
        city_items = sorted(city_item_list[city_index - 1].copy(), key=itemgetter(2))                                   #copy array and sort items by weight(lighter first)

    while city_items.__len__()> 0 and picked_item is None:
        if(basic_info['KNP cap'] - current_cap >= city_items[0][2]):                                                    # if we have cap
            picked_item = city_items[0]
        else:
            city_items.remove(city_items[0])
    return picked_item

# Use this if you know whole item pool before you start moving between cities
def get_list_of_ordered_items(strategy):

    ordered_list=[]
    if (strategy == KNP_greedy_strategies[0]):                                                                          #most expensive
        ordered_list = sorted(get_all_items(),key=itemgetter(1),reverse=True)
    elif(strategy==KNP_greedy_strategies[1]):                                                                           #lightest
        ordered_list = sorted(get_all_items(), key=itemgetter(2))
    elif(strategy == KNP_greedy_strategies[2]):                                                                         #best ratio
                                                                                                                        #[node_index,ratio] X 510
        all_items=get_all_items()
        ratio_result =[None] * all_items.__len__()

        for x in range(all_items.__len__()):
            ratio_result[x] = (all_items[x][1] / all_items[x][2])

        items_ranking = pd.DataFrame()
        items_ranking['solutions'] = all_items
        items_ranking['score'] = ratio_result

        items_ranking.sort_values(by = ['score'], inplace=True, ascending=False)


    solution=[]
    sum_weight = 0
    itr = 0
    if(ordered_list.__len__()>0):                                                                                       # first and second option
        while sum_weight + ordered_list[itr + 1][1] < basic_info['KNP cap']:
            solution.append(ordered_list[itr])
            sum_weight += ordered_list[itr][1]
            itr += 1
    else:                                                                                                               # third - dataframe
        items_ordered_by_ratio = items_ranking['solutions'].tolist()

        next_step_val = 0
        while (next_step_val < basic_info['KNP cap']):
            sum_weight += items_ordered_by_ratio[itr][1]
            itr += 1
            next_step_val = sum_weight + items_ranking['score'][itr]
        solution = items_ordered_by_ratio[:itr]
    return solution


# ['most_expensive','lightest','best_ratio']
#print(get_list_of_ordered_items('best_ratio'))
#print("--- %s seconds ---" % (time.time() - start_time))

items_ordered_me,items_ordered_li,items_ordered_br= get_list_of_ordered_items('most_expensive'),get_list_of_ordered_items('lightest'),get_list_of_ordered_items('best_ratio')



# Sum of picked items - g(y)

def sum_item_values(itemlist):
    return sum(profit for inx , profit , weight in itemlist)


# Travel cost  - f(x,y)
def get_travel_cost(route,list_of_choosed_items):
    travel_cost = 0
    itr =0
    current_cap = 0

    while itr + 1 < len(route):
        travel_cost += get_travel_time(int(route[itr])-1 ,int(route[itr+1])-1,current_cap)
        items_for_city = get_items_for_city(int(route[itr]))
        if (items_for_city is not None):
            for item in items_for_city:
                if(list_of_choosed_items.__contains__(item)):
                    current_cap += item[2]

        itr += 1

    travel_cost += get_travel_time(len(route)-1,0,current_cap)          # Back to first city

    return travel_cost    #Travel_cost

# Getting fitness of a solution - we need to minimalize it
def getFitness(time,sum_value):
    return  time - sum_value

# I'M ONLY RETURNING ROUTE
def crossover_new_route(parent_1, parent_2):
    parent_1 = np.asarray(parent_1)
    parent_2 = np.asarray(parent_2)
    childPath = np.empty(parent_2.shape[0], dtype=np.int)
    start = random.randint(1, int(parent_1.shape[0] / 2))
    end = random.randint(int(parent_1.shape[0] / 2) + 1, parent_1.shape[0] - 1)
    slice = parent_1[start: end]
    childPath[start: end] = slice
    indexesToDelete = np.empty(slice.shape[0], dtype=np.int)
    for i in range(slice.shape[0]):
        for j in range(parent_2.shape[0]):
            if slice[i] == parent_2[j]:
                indexesToDelete[i] = j
    valuesToInsert = np.delete(parent_2, indexesToDelete)
    i = len(childPath) - 1
    lastUsedIndex = len(valuesToInsert) - 1
    while i >= end:
        childPath[i] = valuesToInsert[lastUsedIndex]
        i -= 1
        lastUsedIndex -= 1
    i = start - 1
    while i >= 0:
        childPath[i] = valuesToInsert[lastUsedIndex]
        lastUsedIndex -= 1
        i -= 1
    return childPath.tolist()





# Returns two different values from certain range
def getTwoDiff(range):
    index_1 = random.randint(0, range)
    index_2 = random.randint(0,range)
    while (index_1 == index_2):
        index_2 = random.randint(0,range)
    return index_1,index_2

def getDiff(index_1,range):
    index_2 = random.randint(0,range)
    while (index_1 == index_2):
        index_2 = random.randint(0,range)
    return index_2

def remove_duplicates(x):
  return list(dict.fromkeys(x))