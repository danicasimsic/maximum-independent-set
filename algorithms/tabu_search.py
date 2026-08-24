import random

from .graph import is_independent

def get_conflicting_vertices(graph, solution, vertex):
    # Vraća čvorove iz solution koji su susedi čvora vertex

    return [
        v for v in solution
        if graph[vertex][v] == 1
    ]

# Vraća susedno rešenje najveće veličine
def get_neighbors(graph, solution):
    """
    Generiše susede trenutnog rešenja korišćenjem (k,1)-swap poteza.

    Za svaki mogući novi čvor čuvamo:
    - novo rešenje
    - dodati čvor
    - izbačene čvorove
    - k, odnosno broj izbačenih čvorova
    """
    n = len(graph)
    neighbors = []

    for vertex in range(n):

        if vertex in solution:
            continue

        conflicting_vertices = get_conflicting_vertices(
            graph,
            solution,
            vertex
        )

        new_solution = [
            v for v in solution
            if v not in conflicting_vertices
        ]

        new_solution.append(vertex)

        neighbor = {
             "solution": new_solution,
            "added": vertex,
            "removed": conflicting_vertices,
            "k": len(conflicting_vertices)
        }

        neighbors.append(neighbor)

    return neighbors

def is_tabu(tabu_list, vertex):
    # Proverava da li je čvor trenutno tabu

    return vertex in tabu_list and tabu_list[vertex] > 0

def is_move_tabu(move, tabu_list):
    # Proverava da li je potez tabu.

    # Potez je tabu ako je neki od čvorova
    # koji se izbacuju trenutno tabu.

    for vertex in move["removed"]:
        if is_tabu(tabu_list, vertex):
            return True

    return False

def update_tabu_list(tabu_list):
    #Smanjuje tabu tenure za sve čvorove
    #i uklanja one kojima je tenure istekao

    for vertex in list(tabu_list.keys()):
        tabu_list[vertex] -= 1

        if tabu_list[vertex] <= 0:
            del tabu_list[vertex]

def generate_initial_solution(graph):
    #Generiše početno rešenje kao slučajan maksimalan nezavisan skup
    n = len(graph)

    candidates = list(range(n))
    solution = []

    while candidates:
        vertex = random.choice(candidates)

        solution.append(vertex)

        candidates.remove(vertex)

        neighbors = [
            v for v in candidates
            if graph[vertex][v] == 1
        ]

        for neighbor in neighbors:
            candidates.remove(neighbor)

    return solution


def classify_neighbors(neighbors):
    """
    Razvrstava susede prema broju izbačenih čvorova k.

    NS0 - potezi sa k = 0
    NS1 - potezi sa k = 1
    NS2 - potezi sa k = 2
    NS>2 - potezi sa k > 2
    """

    ns0 = []
    ns1 = []
    ns2 = []
    ns_more = []

    for neighbor in neighbors:

        k = neighbor["k"]

        if k == 0:
            ns0.append(neighbor)

        elif k == 1:
            ns1.append(neighbor)

        elif k == 2:
            ns2.append(neighbor)

        else:
            ns_more.append(neighbor)

    return ns0, ns1, ns2, ns_more

def select_move(neighbors, tabu_list, best_size):
    """
    Bira sledeći potez.

    Prioritet imaju:
    1. potezi sa k = 0
    2. potezi sa k = 1
    3. potezi sa k > 1

    Tabu potezi se preskaču, osim ako vode
    do rešenja boljeg od trenutno najboljeg.
    """

    ns0, ns1, ns2, ns_more = classify_neighbors(neighbors)

    groups = [ns0, ns1, ns2 + ns_more]

    for group in groups:

        allowed_moves = []

        for move in group:

            tabu = is_move_tabu(
                move,
                tabu_list
            )

            move_size = len(move["solution"])

            # Aspiration:
            # dozvoljavamo tabu potez ako daje
            # novo najbolje rešenje.
            if not tabu or move_size > best_size:
                allowed_moves.append(move)

            if allowed_moves:
                return max(
                    allowed_moves,
                    key = lambda move: len(move["solution"])
                )

    return None

def apply_move(move):
    # Primenjuje izabrani potez i vraća novo rešenje

    return move["solution"].copy()

def update_tabu_after_move(tabu_list, move, tenure):
    """
    Dodaje izbačene čvorove u tabu listu.

    Čvorovi koji su izbačeni iz rešenja
    neko vreme ne mogu ponovo da budu dodati.
    """

    for vertex in move["removed"]:
        tabu_list[vertex] = tenure

def tabu_search(graph, iterations = 100, tabu_tenure = 5):
    """
    Tabu Search za problem Maximum Independent Set.

    graph:
        matrica susedstva grafa

    iterations:
        broj iteracija algoritma

    tabu_tenure:
        broj iteracija tokom kojih je izbačeni čvor tabu
    """

    # Početno rešenje
    current_solution = generate_initial_solution(graph)

    # Najbolje pronađeno rešenje
    best_solution = current_solution.copy()

    # Tabu lista
    tabu_list = {}

    for _ in range(iterations):

        # Generišemo susede trenutnog rešenja
        neighbors = get_neighbors(
            graph,
            current_solution
        )

        # Biramo sledeći potez
        move = select_move(
            neighbors,
            tabu_list,
            best_size = len(best_solution)
        )

        # Ako nema dozvoljenog poteza, završavamo
        if move is None:
            break

        # Primeni potez
        current_solution = apply_move(move)

        # Smanji postojeći tabu tenure
        update_tabu_list(tabu_list)

        # Dodaj izbačene čvorove u tabu listu
        update_tabu_after_move(
            tabu_list,
            move,
            tabu_tenure
        )

        # Ažuriraj najbolje rešenje
        if len(current_solution) > len(best_solution):
            best_solution = current_solution.copy()

    return best_solution