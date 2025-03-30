import numpy as np

def single_point_mutation(chromosome):
    """
    Mutates a single random point in the chromosome.
    """
    mutation_point = np.random.randint(len(chromosome.genes))
    chromosome.genes[mutation_point] = not chromosome.genes[mutation_point]

def two_point_mutation(chromosome):
    """
    Mutates two random points in the chromosome.
    """
    points = np.random.choice(range(len(chromosome.genes)), 2, replace=False)
    for point in points:
        chromosome.genes[point] = not chromosome.genes[point]

def boundary_mutation(chromosome):
    """
    Mutates the first or the last gene of the chromosome.
    """
    if np.random.rand() > 0.5:
        # Mutate the first gene
        chromosome.genes[0] = not chromosome.genes[0]
    else:
        # Mutate the last gene
        chromosome.genes[-1] = not chromosome.genes[-1]