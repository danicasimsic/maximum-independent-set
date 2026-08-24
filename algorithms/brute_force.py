from .graph import is_independent
import time

#Brute-force algoritam za Maximum Independent Set

#Proverava sve podskupove čvorova i vraća najveći nezavisan skup

def brute_force_mis(graph):
    n = len(graph)

    best_solution = []

    for mask in range(2 ** n):
        solution = []

        for i in range(n):
            if mask & (1 << i):
                solution.append(i)

        if len(solution) <= len(best_solution):
            continue

        if is_independent(graph, solution):
            best_solution = solution

    return best_solution