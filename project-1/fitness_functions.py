def choose_fitness_function(name):
    """
    Choose the fitness function based on the given name.
    """
    if name == 'hyperellipsoid':
        return hyperellipsoid_function
    elif name == 'hypersphere':
        return hypersphere
    elif name == 'rosenbrock':
        return rosenbrock_function
    else:
        raise ValueError(f"Unknown fitness function: {name}")

def hypersphere(x):
    """
    Fitness function for the hypersphere problem.
    """
    return sum(xi ** 2 for xi in x)

def hyperellipsoid_function(x):
    """
    Fitness function for the hyperellipsoid problem.
    """
    return sum(xi ** 2 for xi in x)

def rosenbrock_function(x):
    """
    Fitness function for the Rosenbrock's valley (banana function).
    """
    return sum(100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2 for i in range(len(x) - 1))