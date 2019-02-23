"""
This module implements local search on a simple abs function variant.
The function is a linear function  with a single, discontinuous max value
(see the abs function variant in graphs.py).

@author: kvlinden
@editor: Ziqi Chen
@CS 344 Lab 2
@Date: Feb 8, 2019
@version 6feb2013
"""
from tools.aima.search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
from threading import Timer
import math
import time


class SineVariant(Problem):
    """
    State: x value for the abs function variant f(x)
    Move: a new x value delta steps from the current x (in both directions) 
    """
    
    def __init__(self, initial, maximum=30.0, delta=0.001):
        self.initial = initial
        self.maximum = maximum
        self.delta = delta
        
    def actions(self, state):
        return [state + self.delta, state - self.delta]
    
    def result(self, stateIgnored, x):
        return x
    
    def value(self, x):
        return math.fabs(x * math.sin(x))


if __name__ == '__main__':

    # Formulate a problem with the absolute value of a sine function and multiple local maxima.
    maximum = 30
    hill_x = 0
    hill_max = 0
    annealing_x = 0
    annealing_max = 0

    for i in range(10):
        #new initial starting point
        initial = randrange(0, maximum)
        p = SineVariant(initial, maximum, delta=1)

        # Solve the problem using hill-climbing.
        hill_solution = hill_climbing(p)

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