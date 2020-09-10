import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from copy import copy
from itertools import combinations
import random

# for trips <= 14
def solve_tsp(city_coordinates, roundtrip=True):
    """Returns the indices of the shortest roundpath.
    Yields an exact solution via a dynamic programming approach.
    Suitable for less than 14 cities."""

    distances = euclidean_distances(city_coordinates)
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(distances[0][1:])}
    cnt = len(distances)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in combinations(range(1, cnt), m)]:
            for j in S - {0}:
                B[(S, j)] = min( [(A[(S-{j},k)][0] + distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    res = min([(A[d][0] + distances[0][d[1]], A[d][1]) for d in iter(A)])
    if roundtrip:
        return res[1] + [res[1][0]]
    else:
        return res[1]


# for trips >= 14
def approximate_tsp(city_coordinates, roundtrip=True):
    """Returns the indices of an estimate of the shortest roundpath.
    Yields a solution via simulated annealing.
    Suitable more than 14 cities."""

    city_coordinates = np.array(city_coordinates)
    num_cities = len(city_coordinates)
    x = range(num_cities)
    tour = random.sample(range(num_cities),num_cities)
    factor = 100./city_coordinates.mean()
    city_coordinates = city_coordinates*factor

    for temperature in np.logspace(0,1,num=10000)[::-1]:
        # swap two random cities and see if it's better
        i,j = np.random.choice(x, 2)
        newTour = copy(tour)
        newTour[j], newTour[i] = newTour[i], newTour[j]
        oldDistance = np.sum(np.sqrt(np.sum(np.diff(city_coordinates[tour], axis=0)**2, axis=1)))
        newDistance = np.sum(np.sqrt(np.sum(np.diff(city_coordinates[newTour], axis=0)**2, axis=1)))
        if np.exp((oldDistance - newDistance) / temperature) > np.random.random():
            tour = copy(newTour)    
    if roundtrip:
        return tour + [tour[0]]
    else:
        return tour