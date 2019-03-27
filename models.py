import random
import tools


class Solution():
    def __init__(self,route,strategy):
        self.route = route
        self.strategy = strategy


    def __str__(self):
        return ( ' Route: ' + str(self.route)  +'  Strategy: ' + str(self.strategy))

    def mutate(self):
        route = self.route
        index_1, index_2 = tools.getTwoDiff(route.__len__() - 1)

        route[index_1], route[index_2] = route[index_2], route[index_1]

        if (random.randint(0, 101) <= 2):  # Super mutation chance
            index_1, index_2 = tools.getTwoDiff(route.__len__() - 1)
            route[index_1], route[index_2] = route[index_2], route[index_1]

        self.route = route

