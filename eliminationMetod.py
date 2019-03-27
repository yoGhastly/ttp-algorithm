import random
import tools
import numpy as np
import pandas as pd

def roulette(solution_ranking,how_many):

    new_solutions = pd.DataFrame()
    new_solutions['score'] = []
    new_solutions['solutions'] = []
    while(new_solutions.__len__() < solution_ranking.__len__()):

        solution_ranking.sort_values(by=['score'], ascending=True,inplace=True)
        max_val = np.abs(max(solution_ranking['score']))
        sum=0
        circle = np.empty(shape=solution_ranking.__len__())
        for x in range(circle.__len__()):
            sum +=  np.abs(solution_ranking['score'][x]) - max_val
            circle[x] = sum

        circle = circle/np.sum(circle)


        sum = circle[0]
        for x in range (circle.shape[0]):
            sum += circle[x]
            circle[x] = sum


        for x in range(how_many):
            picked_percentage = random.random()
            itr = 0
            while(picked_percentage > circle[itr] and itr <= circle.shape[0]-1):
                itr+=1

        champion_sol = solution_ranking['solutions'][itr]
        champion_score = solution_ranking['score'][itr]

        champ_frame = pd.DataFrame()
        champ_frame['solutions'] = [champion_sol]
        champ_frame['score'] = [champion_score]

        new_solutions = pd.concat([new_solutions, champ_frame]).reset_index(drop=True)



    return new_solutions



def tournament(solution_ranking,tour):
    index_pool_vals=list(solution_ranking.index.values)
    new_solutions = pd.DataFrame()
    new_solutions['score']=[]
    new_solutions['solutions']=[]
    while(new_solutions.__len__() < solution_ranking.__len__()):
        index_pool = index_pool_vals.copy()
        to_drop = []
        for i in range(tour):
            picked= random.choice(index_pool)
            to_drop.append(picked)
            index_pool.remove(picked)

        best = solution_ranking['score'][to_drop[0]]    # best means lowest

        champion = to_drop[0]
        for x in to_drop:
            if(best>solution_ranking['score'][x]):
                best = solution_ranking['score'][x]
                champion = x

        champion_sol = solution_ranking['solutions'][champion]
        champion_score = solution_ranking['score'][champion]

        champ_frame = pd.DataFrame()
        champ_frame['solutions'] = [champion_sol]
        champ_frame['score'] = [champion_score]

        new_solutions = pd.concat([new_solutions,champ_frame]).reset_index(drop=True)

    return new_solutions