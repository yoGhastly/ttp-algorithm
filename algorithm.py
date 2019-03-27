# or rather metaheuristic :)

import random
import pandas as pd
import numpy as np
import time
#import matplotlib.pyplot as plt

import tools
import eliminationMetod
from models import Solution


items_sorted_strategy = \
    {
        'best_ratio':tools.get_list_of_ordered_items('best_ratio'),
        'most_expensive':tools.get_list_of_ordered_items('most_expensive'),
        'lightest':tools.get_list_of_ordered_items('lightest')
    }





def initialize(size_of_population):
    population = []

    for x in range(size_of_population):
        random_solution = tools.generate_TSP_solution()
        random_strategy = random.choice(tools.KNP_greedy_strategies)
        #t_cost = tools.get_travel_cost(random_solution,random_strategy)

        population.append(Solution(random_solution, random_strategy ))
    return population



#Get score for each solution
def evaluate(solution_ranking):
    for x in range (solution_ranking.__len__()):
        solution_strategy = solution_ranking['solutions'][x].strategy
        item_profit = tools.sum_item_values(items_sorted_strategy[solution_strategy])
        travel_time = tools.get_travel_cost(solution_ranking['solutions'][x].route,items_sorted_strategy[solution_strategy])
        solution_ranking['score'][x] = travel_time - item_profit
    return solution_ranking.sort_values(by=['score'], ascending=False).reset_index(drop=True)                           #return sorted by score

def crossing_over(solution_ranking, percenate_of_cross):
    solution_ranking.reset_index(drop=True,inplace=True)

    solutions_to_cross = list(solution_ranking.index.values)

    for parent_index_1 in solutions_to_cross:
        if(random.random() < percenate_of_cross):
            parent_index_2 = tools.getDiff( parent_index_1, solution_ranking.__len__() - 1)

            child_route = tools.crossover_new_route(solution_ranking['solutions'][parent_index_1].route,solution_ranking['solutions'][parent_index_2].route)
            random_strategy = random.choice([solution_ranking['solutions'][parent_index_1].strategy,solution_ranking['solutions'][parent_index_2].strategy])

            solution_ranking['score'][parent_index_1] = 0
            solution_ranking['solutions'][parent_index_1] = Solution(child_route, random_strategy)

    '''
    solution_ranking.drop(solutions_to_cross,inplace=True)                                                              #remove parents

    new_solutions = pd.DataFrame()
    new_solutions['solutions'] = solutions_children
    new_solutions['score'] = score_list
    new_solutions.index = np.arange(solution_ranking.__len__(), solution_ranking.__len__() +new_solutions.__len__())    #reindexing new solutions
    '''
    return solution_ranking                                                                  #return merged old and new solutions

def mutate(solution_ranking,chance_of_mutation):                                                                     #chance_of_mut range 0.00 - 1.00
        solution_ranking.reset_index(drop=True, inplace=True)
        for x in range (solution_ranking.__len__()):
            if(random.random() < chance_of_mutation):
                solution_ranking['solutions'][x].mutate()
        return solution_ranking


def refill(solution_ranking,size_of_population):
    solution_ranking.reset_index(drop=True, inplace=True)
    solutions = []
    score_list = []

    while ( solution_ranking.__len__() + solutions.__len__()  <  size_of_population):  # generating solutions till num of pop

        child_route = tools.generate_TSP_solution()
        random_strategy = random.choice(tools.KNP_greedy_strategies)
        solution = Solution( child_route, random_strategy)
        solutions.append(solution)
        score_list.append(0)  # eval later on

    new_solutions = pd.DataFrame()
    new_solutions['solutions'] = solutions
    new_solutions['score'] = score_list
    new_solutions.index = np.arange(solution_ranking.__len__(),solution_ranking.__len__() + new_solutions.__len__())  # reindexing new solutions


    return (pd.concat([solution_ranking,new_solutions])).reset_index(drop=True)

def eliminate(method,solution_ranking,ratio):
    if(method=='roulette'):
        return eliminationMetod.roulette(solution_ranking,ratio)
    elif(method=='tournament'):

        return eliminationMetod.tournament(solution_ranking,ratio)



def evolution(size_of_population,num_of_generations,elim_type,cross_chance,tour,chance_of_mutation):

    population = initialize(size_of_population)
    solution_ranking = pd.DataFrame()
    solution_ranking['solutions'] = population
    solution_ranking['score'] = np.empty(shape=(size_of_population , 1), dtype=float).tolist()

    generations = pd.DataFrame(index=np.arange(0,num_of_generations), columns=['AVG','MIN','MAX'])
    generations = generations.fillna(0)

    for x in range (num_of_generations):
        start_time = time.time()
        solution_ranking = evaluate(solution_ranking)

        generations['AVG'][x] = solution_ranking['score'].mean()
        generations['MIN'][x] = solution_ranking['score'].min()
        generations['MAX'][x] = solution_ranking['score'].max()

        solution_ranking = eliminate(elim_type,solution_ranking, tour)
        solution_ranking = crossing_over(solution_ranking,cross_chance)
        solution_ranking = mutate(solution_ranking,chance_of_mutation)
        print("--- %s seconds ---" % (time.time() - start_time))

    print(generations)
    generations.to_csv('mid_1'+elim_type+'_g_'+str(num_of_generations)+'p'+str(size_of_population)+'_cr_'
   +str(cross_chance) +'_t_'+str(tour)+'_m_'+str(chance_of_mutation),sep='\t')




#evolution(10,50,'tournament',0.7,5,0.01)


def greedy_solution():
    distance_matrix = tools.distance_array
    index_pool = np.arange(0,distance_matrix.shape[0])
    index_pool = list(index_pool)
    current_city = np.random.choice(index_pool)
    already_visited = []


    while (already_visited.__len__() < distance_matrix.shape[0]):

        randomInx= random.choice(index_pool)
        min = distance_matrix[current_city][randomInx]
        picked_inx = randomInx
        while (min == 0):
            randomInx = random.choice(index_pool)
            min = distance_matrix[current_city][randomInx]
            picked_inx = randomInx
        for y in index_pool:

            if (distance_matrix[current_city][y] < min and distance_matrix[current_city][y]>0):

                    if(not already_visited.__contains__(y)):
                        min = distance_matrix[current_city][y]
                        picked_inx = y

        already_visited.append(picked_inx)
        current_city = picked_inx
        index_pool.remove(picked_inx)

    return np.asarray(already_visited)

#print(tools.get_travel_cost(greedy_solution(),'best_ratio'))