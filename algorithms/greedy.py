from .graph import is_independent

# Pronalazenje nezavisnog skupa Greedy heuristikom
# U svakom koraku bira čvor najmanjeg stepena među preostalim čvorovima
def greedy_mis(graph):
    n = len(graph)

    remaining = set(range(n))
    solution = []

    while remaining:

        # Biramo čvor najmanjeg stepena
        vertex = min(
            remaining,
            key = lambda v: sum(graph[v][u] for u in remaining)
        )

        # Dodajemo ga u rešenje
        solution.append(vertex)

        # Uklanjamo iz kandidata čvor i njegove susede
        neighbors = {
            u for u in remaining
            if graph[vertex][u] == 1
        }


        remaining.remove(vertex)
        remaining -= neighbors

    return solution
