import cplex


def cplex_mis(graph):
    n = len(graph)

    model = cplex.Cplex()

    # Isključujemo CPLEX ispis
    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    # Binarne promenljive x_i
    variable_names = [f"x_{i}" for i in range(n)]

    model.variables.add(
        names=variable_names,
        types=[model.variables.type.binary] * n
    )

    # Maksimizujemo broj izabranih čvorova
    model.objective.set_sense(model.objective.sense.maximize)

    model.objective.set_linear(
        [(f"x_{i}", 1.0) for i in range(n)]
    )

    # Za svaku granu (i, j):
    # x_i + x_j <= 1
    constraints = []

    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                constraints.append(
                    cplex.SparsePair(
                        ind=[f"x_{i}", f"x_{j}"],
                        val=[1.0, 1.0]
                    )
                )

    if constraints:
        model.linear_constraints.add(
            lin_expr=constraints,
            senses=["L"] * len(constraints),
            rhs=[1.0] * len(constraints)
        )

    # Rešavanje
    model.solve()

    # Izabrani čvorovi
    values = model.solution.get_values()

    solution = [
        i for i in range(n)
        if values[i] > 0.5
    ]

    return solution