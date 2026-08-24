import numpy as np

#Provera da li je solution nezavisan skup

# graph - matrica susedstva grafa
# solution - lista indeksa cvorova koji su izabrani
def is_independent(graph, solution):

    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            u = solution[i]
            v = solution[j]

            if graph[u][v] == 1:
                return False

    return True


#velicina nezavisnog skupa
def solution_size(solution):
    return len(solution)

import numpy as np

#generisanje slucajnog neusmerenog grafa sa n cvorova
# p - verovatnoca da postoji grana izmedju dva cvora
def generate_random_graph(n, p):

    graph = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            if np.random.random() < p:
                graph[i][j] = 1
                graph[j][i] = 1

    return graph