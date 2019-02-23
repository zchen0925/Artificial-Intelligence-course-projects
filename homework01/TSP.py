"""
This module implements local search on a simple abs function variant.
The function is a linear function  with a single, discontinuous max value
(see the abs function variant in graphs.py).

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


class TravelingSalesman(Problem):
    """
    State: x value for the abs function variant f(x)
    Move: a new x value delta steps from the current x (in both directions) 
    """
    def __init__(self, initial, map):
        self.initial = initial
        self.map = map
        
    def actions(self, state):
        return [state + self.delta, state - self.delta]
    
    def result(self, state, action):
        return state
    
    def value(self, state):
        """
        :param state: the current city circuit
        :return: the sum of the travelling distances in the given state, negated in order to reflect value
        """
        total = 0
        i = 1
        while i < len(state):
            try:
                total += self.map[state[i-1], state[i]]
            except:
                total += self.map[state[i], state[i-1]]
            i += 1
        return total





if __name__ == '__main__':

    # Formulate a problem with the absolute value of a sine function and multiple local maxima.
    maximum = 30
    hill_x = 0
    hill_max = 0
    annealing_x = 0
    annealing_max = 0


    initial = [0,1,2,3,4,5,0]
    map = {(0,1): 1.5, (0,2): 2, (0,3): 3, (0,4): 2.5, (0,5): 3,
           (1,2): 7, (1,3): 2.4, (1,4): 4, (1,5): 3.6,
           (2,3): 5,(2,4): 4.5, (2,5): 1.5,
           (3,4): 2.5, (3,5): 3,
           (4,5): 7.5}
    tsp = TravelingSalesman(initial, map)

    test = [1,4,2,5,3,5,0]

    print("testing value function", tsp.value(test))

    """
    for i in range(10):
        #new initial starting point
        # Solve the problem using hill-climbing.
        hill_solution = hill_climbing(tsp)


        if p.value(hill_solution)>hill_max:
            hill_max = p.value(hill_solution)
            hill_x = hill_solution
            
        

        # Solve the problem using simulated annealing.
        start_time = time.time()
        annealing_solution = simulated_annealing(
            p,
            exp_schedule(k=20, lam=0.005, limit=1000)
        )

    #    print ("Simulated annealing took --- %s seconds ---" % (time.time()-start_time))
        if p.value(annealing_solution)>annealing_max:
            annealing_max = p.value(annealing_solution)
            annealing_x = annealing_solution

    print('Hill-climbing solution       x: ' + str(hill_x)
          + '\tvalue: ' + str(hill_max)
          )

    print('Simulated annealing solution x: ' + str(annealing_x)
          + '\tvalue: ' + str(annealing_max)
          )

        hill_solution = hill_climbing(p)
        print('Hill-climbing solution       x: ' + str(hill_solution)
              + '\tvalue: ' + str(p.value(hill_solution))
              )

        # Solve the problem using simulated annealing.
        annealing_solution = simulated_annealing(
            p,
            exp_schedule(k=20, lam=0.005, limit=1000)
        )
        print('Simulated annealing solution x: ' + str(annealing_solution)
              + '\tvalue: ' + str(p.value(annealing_solution))
              )
"""