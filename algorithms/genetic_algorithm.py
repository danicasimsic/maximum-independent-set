import random
import copy 

from .graph import is_independent

class Individual:
    # "Jedinka genetskog algoritma"
    # code predstavlja jedno rešenje MIS problema

    def __init__(self, graph):

        self.graph = graph
        self.n = len(graph)

        # Nasumično početno rešenje
        self.code = [
            random.random() < 0.5
            for _ in range(self.n)
        ]

        self.calc_fitness()

    def calc_fitness(self):

        # Broj izabranih čvorova
        selected = [
            i for i in range(self.n)
            if self.code[i]
        ]

        # Broj konflikata:
        # parova izabranih čvorova između kojih postoji grana
        conflicts = 0

        for i in range(len(selected)):
            for j in range(i+1, len(selected)):

                u = selected[i]
                v = selected[j]

                if self.graph[u][v]:
                    conflicts += 1

        # Bäck-Khuri fitness funkcija
        self.fitness = len(selected) - self.n * conflicts

def selection(population):
    # Proporcionalna selekcija (roulette-wheel selection)

    min_fitness = min(
        individual.fitness
        for individual in population
    )

    # Fitness može biti negativan, pa ga pomeramo
    if min_fitness <= 0:
        shift = -min_fitness + 1
    else:
        shift = 0

    weights = [
        individual.fitness + shift
        for individual in population
    ]

    return random.choices(
        population,
        weights = weights,
        k = 1
    )[0]

def crossover(parent1, parent2):
    # Two-point crossover

    n = parent1.n

    point1, point2 = sorted(
        random.sample(range(1, n), 2)
    )

    code1 = (
        parent1.code[:point1] 
        + parent2.code[point1:point2]
        + parent1.code[point2:]
    )
    code2 = (
        parent2.code[:point1] 
        + parent1.code[point1:point2]
        + parent2.code[point2:]
    )

    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    child1.code = code1
    child2.code = code2
    return child1, child2

def mutation(individual, mutation_rate):
    # Mutira jedinku promenom bitova u njenom kodu
    # Mutacija uvodi novu raznovrsnost

    # Mutation rate - verovatnoća mutacije svakog gena
    for i in range(individual.n):

        if random.random() < mutation_rate:
            individual.code[i] = not individual.code[i]

    individual.calc_fitness()

def genetic_algorithm(
        graph,
        population_size = 50,
        max_evaluations=20000,
        crossover_rate = 0.6
):
    # Genetski algoritam za Maximum Independent Set

    n = len(graph)

    # Bäck-Khuri: pm = 1/n
    mutation_rate = 1 / n

    # Početna populacija
    population = [
        Individual(graph)
        for _ in  range(population_size)
    ]
    evaluations = population_size

    # Najbolje validno rešenje
    empty_solution = Individual(graph)
    empty_solution.code = [False] * n
    empty_solution.calc_fitness()

    best_feasible = empty_solution

    # Proveravamo početnu populaciju
    for individual in population:

        selected = [
            i for i in range(individual.n)
            if individual.code[i]
        ]

        if is_independent(graph, selected):

            if individual.fitness > best_feasible.fitness:
                best_feasible = copy.deepcopy(individual)

    while evaluations + population_size <= max_evaluations:

        new_population = []

        while len(new_population) < population_size:

            # Biramo roditelje
            parent1 = selection(population)
            parent2 = selection(population)

            # Ukrštanje
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                # Ako nema ukrštanja, deca su kopije roditelja
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)


            # Mutacija
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)

            # Dve nove evaluacije
            evaluations += 2

            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

        # Tražimo najbolje validno rešenje
        for individual in population:

            selected = [
                i for i in range(individual.n)
                if individual.code[i]
            ]

            if is_independent(graph, selected):
                if individual.fitness > best_feasible.fitness:
                    best_feasible = copy.deepcopy(individual)


    return [
        i for i in range(best_feasible.n)
        if best_feasible.code[i]
    ]