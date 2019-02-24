"""
This module implements local search on a traveling salesman problem.
@author: Ziqi Chen
@CS 344 Homework 1
@Date: Feb 22, 2019
"""
from tools.aima.search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
from threading import Timer
import math
import time

debug = 0
class TravelingSalesman(Problem):
    """
    initial: a random complete city circuit.
    map: a dictionary containing the distances between any two cities in the circuit.
    """
    def __init__(self, numCities, initial, map):
        self.num = numCities
        self.initial = initial
        self.map = map

    # actions returns a list of pairs of cities to swap in the current state
    def actions(self, state):
        """
        :param state: the current state containing a circuit
        :return: actions, a list containing tuples of pairs of cities to swap order in the circuit. The list contains all possible swaps
        """
        actions = []
        lastCity = max(state)
        i = 1
        while i < (len(state)-2) :
            currentCity = state[i]
            for selectSwap in range(1, lastCity+1):
                if currentCity != selectSwap:
                    actions.append([currentCity, selectSwap])
            i += 1
        return actions

    def result(self, state, action):
        """
        :param state: current state in the tsp
        :param action: a selected action (pair of cities to swap)
        :return: the new state resulting from swapping the selected pair of cities to the given state
        """
        new_state = state[:]
        swap_1 = state.index(action[0])
        swap_2 = state.index(action[1])
        new_state[swap_1] = action[1]
        new_state[swap_2] = action[0]
        return new_state

    def value(self, state):
        """
        :param state: the current city circuit
        :return: the sum of the travelling distances in the given state, negated in order to reflect value
        distances should be symmetric
        """
        total = 0
        for i in range(1, numCities+1):
            first = state[i-1]
            second = state[i]
            try:
                dist = self.map[(first, second)]
            except:
                dist = self.map[(second, first)]
        # the shortest past is the best, so distances are negated to reflect this.
            total -= dist
            if debug:
                print("current cities: ", first, second, "distance between cities: ", dist)
        return total

if __name__ == '__main__':
    numCities = 50
    initial = []
    for city in range(numCities):
        initial.append(city)
    initial.append(0)

    map = {}
    for cityA in range(numCities):
        for cityB in range(cityA+1, numCities):
            map[cityA, cityB] = randrange(1, 20)

    '''
    map = {(0,1): 1.5, (0,2): 2, (0,3): 3, (0,4): 2.5, (0,5): 3,
           (1,2): 7, (1,3): 2.4, (1,4): 4, (1,5): 3.6,
           (2,3): 5,(2,4): 4.5, (2,5): 1.5,
           (3,4): 2.5, (3,5): 3,
           (4,5): 7.5}
    '''

    if debug:
        print("testing the constructed map: ", map)

    tsp = TravelingSalesman(numCities, initial, map)
    print("Traveling salesman problem: ",
          "\ninitial circuit: ", initial,
          "initial circuit distance: ", -tsp.value(initial))

    hill_solution = hill_climbing(tsp)
    print("Hill-climbing solution: ", str(hill_solution), "distance: ", str(-tsp.value(hill_solution)))

    annealing_solution = simulated_annealing(tsp,
        exp_schedule(k=20, lam=0.005, limit=10000)
    )
    print("Simulated solution: ", str(annealing_solution), "distance: ", str(-tsp.value(annealing_solution)))
