"""
This module formulates a course scheduling problem using the CSP formulation and offers a scheduling solution for cs courses.

@author: zc23
@CS 344 Homework01
"""

import time

from csp import CSP, parse_neighbors, min_conflicts, backtracking_search, AC3
from search import depth_first_graph_search

debug = 0
def courseScheduling(courses = 'cs108 cs112 cs212 cs214 cs232 cs344 cs352', faculty = 'dschuurman hplantinga jadams kvanderlinden', times = 'mwf800 mwf900 mwf1030 mwf230 tth1030', classrooms = 'nh253 sb382', assignments = {'cs108':['jadams', 'kvanderlinden', 'dschuurman'], 'cs344':['kvanderlinden'], 'cs352':['hplantinga']}):
    """
    :param courses: will be the variables in CSP formulation
    :param faculty:
    :param times:
    :param classrooms:
    :param assignments: a dict containing professors who are assigned to a course. Not all courses have assigned professors
    :return: a CSP instance with variables populated with course numbers, domains populated with any possible combinations of prof+time+location for each course, neighbors populated with any course pairings, and constraints see comments below
    """
    variables = courses.split()
    faculty = faculty.split()
    times = times.split()
    classrooms = classrooms.split()
    assignments = assignments
    domains = {}
    neighbors = {}

    def findAssignments(faculty=faculty, times = times, classrooms = classrooms):
        possibilities = []
        for prof in faculty:
            for time in times:
                for room in classrooms:
                    possibilities.append(prof+' '+time+' '+room)
        return possibilities

    for course in variables:
        neighbors[course] = [others for others in variables if others != course]
        domains[course] = findAssignments()

    if debug:
        print("testing variables: ", str(variables))
        print("testing domain: ", str(domains))
        print("testing neighbors: ", str(neighbors))

    def scheduling_constraint(A, a, B, b):
        """
        :param A: variable A (a course)
        :param a: the current assigned values for A in domain
        :param B: variable B (a course)
        :param b: the current assigned values for B in domain
        :return: true if all physical constraints and preferred prof-course pairings are satisfied
        no professor teaches two courses at the same time.
        no two courses share the same location at the same time.
        """
        profA = a.split()[0]
        profB = b.split()[0]
        tA = a.split()[1]
        tB = b.split()[1]
        rA = a.split()[2]
        rB = b.split()[2]
        if A in assignments and profA not in assignments[A]:
            return False
        elif B in assignments and profB not in assignments[B]:
            return False
        elif tA == tB:
            if profA == profB or rA == rB:
                return False
            else:
                return True
        else:
            return True


    return CSP(variables, domains, neighbors, scheduling_constraint)

if __name__ == '__main__':
    '''
    tried to solve scheduling problem with AC3, backtracking, and min_conflicts.
    Mirrored printing of results from lab03/queens.py
    '''
    problem = courseScheduling()
    #solution = AC3(problem)
    #solution = backtracking_search(problem)
    solution = min_conflicts(problem)
    if type(solution) is bool:
        if solution and problem.goal_test(problem.infer_assignment()):
            print('AC3 Solution:')
        else:
            print('AC Failure:')
        print(problem.curr_domains)

    # Handle other solutions next.
    elif solution != None and problem.goal_test(solution):
        print('Solution:')
        #i used .format command as seen from this page: https://stackoverflow.com/questions/10837017/how-do-i-make-a-fixed-size-formatted-string-in-python
        print('Course:                  Professor:               Time:                Location:       ')
        for course in solution:
            prof =solution[course].split()[0]
            time = solution[course].split()[1]
            location = solution[course].split()[2]
            print('{:25s}{:25s}{:25s}{:25s}'.format(course,prof,time,location))
    #    problem.display(problem.infer_assignment())
    else:
        print('Failed - domains: ' + str(problem.curr_domains))
        problem.display(problem.infer_assignment())

