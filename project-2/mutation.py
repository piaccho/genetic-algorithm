import numpy as np

def uniform_mutation(chromosome, mutation_rate=0.1):
    """
    Mutacja równomierna: każdy gen ma szansę na zmianę na losową wartość.
    """
    for i in range(len(chromosome.genes)):
        if np.random.rand() < mutation_rate:
            chromosome.genes[i] = np.random.randint(0, 11)

def gaussian_mutation(chromosome, mutation_rate=0.1, sigma=1.0):
    """
    Mutacja Gaussa: każdy gen jest modyfikowany o szum Gaussa z prawdopodobieństwem mutation_rate.
    """
    for i in range(len(chromosome.genes)):
        if np.random.rand() < mutation_rate:
            chromosome.genes[i] += int(np.random.normal(0, sigma))
            chromosome.genes[i] = np.clip(chromosome.genes[i], 0, 10)