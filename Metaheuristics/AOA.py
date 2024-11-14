import numpy as np

def iterarAOA(max_iterations, current_iteration, solutions, bestSolution):
    # Convertir soluciones a un arreglo de NumPy si es una lista
    solutions = np.array(solutions)
    bestSolution = np.array(bestSolution)

    # Inicializar las posiciones de la solución
    new_solutions = np.copy(solutions)

    max_mop = 1
    min_mop = 0.2
    alpha = 5
    mu = 0.499
    upper_bound = 1
    lower_bound = 0

    mop = 1 - ((current_iteration) ** (1 / alpha) / (max_iterations) ** (1 / alpha))  # Ratio de probabilidad
    moa = min_mop + current_iteration * ((max_mop - min_mop) / max_iterations)  # Función acelerada

    num_solutions = solutions.shape[0]
    dimension = solutions.shape[1]

    for i in range(num_solutions):
        for j in range(dimension):
            r1 = np.random.rand()
            if r1 < moa:
                r2 = np.random.rand()
                if r2 > 0.5:
                    new_solutions[i, j] = bestSolution[j] / (mop + np.finfo(float).eps) * ((upper_bound - lower_bound) * mu + lower_bound)
                else:
                    new_solutions[i, j] = bestSolution[j] * mop * ((upper_bound - lower_bound) * mu + lower_bound)
            else:
                r3 = np.random.rand()
                if r3 > 0.5:
                    new_solutions[i, j] = bestSolution[j] - mop * ((upper_bound - lower_bound) * mu + lower_bound)
                else:
                    new_solutions[i, j] = bestSolution[j] + mop * ((upper_bound - lower_bound) * mu + lower_bound)

        Flag_UB = new_solutions[i, :] > upper_bound  # Comprobar si exceden los límites superiores
        Flag_LB = new_solutions[i, :] < lower_bound  # Comprobar si exceden los límites inferiores
        new_solutions[i, :] = (new_solutions[i, :] * (~(Flag_UB | Flag_LB))) + upper_bound * Flag_UB + lower_bound * Flag_LB

    return new_solutions
