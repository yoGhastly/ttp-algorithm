import random

import tools


class Solution():
    def __init__(self,index,route,item_list,travel_time,strategy):
        self.index = index
        self.route = route
        self.item_list = item_list
        self.travel_time = travel_time
        self.strategy = strategy


    def __str__(self):
        return ( 'Index: ' + str(self.index) + ' Route: ' + str(self.route) + ' Travel time: ' + str(self.travel_time) +'  Strategy: ' + str(self.strategy))

    def mutate(self):
        route = self.route
        index_1, index_2 = tools.getTwoDiff(route.__len__() - 1)

        route[index_1], route[index_2] = route[index_2], route[index_1]

        if (random.randint(0, 101) <= 2):  # Super mutation chance
            index_1, index_2 = tools.getTwoDiff(route.__len__() - 1)
            route[index_1], route[index_2] = route[index_2], route[index_1]

        self.route = route

