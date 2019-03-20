# or rather metaheuristic :)
import cProfile
import random
import pandas as pd
import numpy as np
import tools
from models import Solution




def initialize(size_of_population):
    population = np.empty(shape=(size_of_population, 1), dtype=object)

    for x in range(size_of_population):
        random_solution = tools.generate_TSP_solution()
        random_strategy = random.choice(tools.KNP_greedy_strategies)
        t_cost = tools.get_travel_cost(random_solution,random_strategy)

        population[x] = Solution(x, random_solution, t_cost, random_strategy )
    return population



#Get score for each solution
def evaluate(solution_ranking):
    for x in range (solution_ranking.__len__()):
        solution_strategy = solution_ranking['solutions'][x][0].strategy
        item_profit = tools.sum_item_values(tools.get_list_of_ordered_items(solution_strategy))
        travel_time = solution_ranking['solutions'][x][0].travel_time
        solution_ranking['score'][x] = tools.getFitness(travel_time,item_profit)
    return solution_ranking.sort_values(by=['score'], ascending=False).reset_index(drop=True)                           #return sorted by score

def crossing_over(solution_ranking,size_of_population):
    solution_ranking = solution_ranking.reset_index(drop=True)
    solutions = []
    score_list = []

    max_sol_index = 0

    for x in range(solution_ranking.__len__()):                                                                         #Find max(SolutionIndex)
        if(solution_ranking['solutions'][x][0].index > max_sol_index):
            max_sol_index = solution_ranking['solutions'][x][0].index

    while(solution_ranking.__len__() + solutions.__len__() < size_of_population):                                       #generating solutions via crossing-over
        parent_index_1, parent_index_2 = tools.getTwoDiff(solution_ranking.__len__() - 1)

        child_route = tools.crossover_new_route(solution_ranking['solutions'][parent_index_1][0].route,solution_ranking['solutions'][parent_index_2][0].route)
        random_strategy = random.choice([solution_ranking['solutions'][parent_index_1][0].strategy,solution_ranking['solutions'][parent_index_2][0].strategy])
        t_cost = tools.get_travel_cost(child_route,random_strategy)
        solution = Solution(max_sol_index, child_route, t_cost, random_strategy)
        solutions.append([solution])                                                                                    #need to put in into list -

        solution_strategy = solution_ranking['solutions'][x][0].strategy
        item_profit = tools.sum_item_values(tools.get_list_of_ordered_items(solution_strategy))

        score_list.append(tools.getFitness(solution.travel_time,item_profit))                                                                                       # hard to shortly explain
        max_sol_index += 1


    new_solutions = pd.DataFrame()
    new_solutions['solutions'] = solutions
    new_solutions['score'] = score_list
    new_solutions.index = np.arange(solution_ranking.__len__(), solution_ranking.__len__() +new_solutions.__len__())    #reindexing new solutions

    return pd.concat([solution_ranking,new_solutions])                                                                  #return merged old and new solutions

def mutate(solution_ranking,chance_of_mutation):                                                                        #chance_of_mut range 0.00 - 1.00
        for x in range (solution_ranking.__len__()):
            if(random.random() < chance_of_mutation):
                solution_ranking['solutions'][x][0].mutate()
        return solution_ranking

def evolution(size_of_population,num_of_generations,tour_precentage,chance_of_mutation):

    population = initialize(size_of_population)

    solution_ranking = pd.DataFrame()
    solution_ranking['solutions'] = population.tolist()
    solution_ranking['score'] = np.empty(shape=(size_of_population , 1), dtype=float).tolist()

    generations = pd.DataFrame(index=np.arange(0,num_of_generations), columns=['AVG','MIN','MAX'])
    generations = generations.fillna(0)

    for x in range (num_of_generations):
        solution_ranking = evaluate(solution_ranking)

        solution_ranking = tools.tournament(solution_ranking, tour_precentage)

        solution_ranking = crossing_over(solution_ranking,size_of_population)

        solution_ranking = mutate(solution_ranking,chance_of_mutation)

        generations['AVG'][x] = solution_ranking['score'].mean()
        generations['MIN'][x] = solution_ranking['score'].min()
        generations['MAX'][x] = solution_ranking['score'].max()

    print(generations)

evolution(100,100,0.20,0.07)


