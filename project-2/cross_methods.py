import numpy as np
from real_chromosome import RealChromosome

def arithmetic_crossover(parent1, parent2, alpha=0.5):
    """
    Krzyżowanie arytmetyczne: mieszanie genów z użyciem wagi alpha.
    """
    child1_genes = (alpha * parent1.genes + (1 - alpha) * parent2.genes).astype(int)
    child2_genes = ((1 - alpha) * parent1.genes + alpha * parent2.genes).astype(int)
    return RealChromosome(len(parent1.genes)).set_genes(child1_genes), RealChromosome(len(parent2.genes)).set_genes(child2_genes)

def linear_crossover(parent1, parent2, fitness_function):
    """
    Krzyżowanie liniowe: tworzenie trzech dzieci i wybieranie najlepszych na podstawie oceny fitness.
    """

    child1_genes = (0.5 * parent1.genes + 0.5 * parent2.genes).astype(int)
    child2_genes = (1.5 * parent1.genes - 0.5 * parent2.genes).astype(int)
    child3_genes = (-0.5 * parent1.genes + 1.5 * parent2.genes).astype(int)

    children = [
        RealChromosome(len(parent1.genes)).set_genes(child1_genes),
        RealChromosome(len(parent2.genes)).set_genes(child2_genes),
        RealChromosome(len(parent1.genes)).set_genes(child3_genes),
    ]

    # Sort children using the fitness function
    children.sort(key=lambda child: fitness_function(child.genes), reverse=True)
    return children[0], children[1]

def alpha_crossover(parent1, parent2, alpha=0.3):
    """
    Krzyżowanie mieszające typu alfa.
    """ 
    # Calculate gene-wise min and max
    min_genes = np.minimum(parent1.genes, parent2.genes)
    max_genes = np.maximum(parent1.genes, parent2.genes)
    
    # Calculate the difference (d_i)
    d_i = max_genes - min_genes
    
    # Calculate the expanded ranges
    lower_bound = min_genes - alpha * d_i
    upper_bound = max_genes + alpha * d_i
    
    # Generate random values within the expanded ranges for both children
    child1_genes = np.random.uniform(lower_bound, upper_bound, size=parent1.genes.shape).astype(int)
    child2_genes = np.random.uniform(lower_bound, upper_bound, size=parent2.genes.shape).astype(int)
    return RealChromosome(len(parent1.genes)).set_genes(child1_genes), RealChromosome(len(parent2.genes)).set_genes(child2_genes)

def alpha_beta_crossover(parent1, parent2, alpha=0.3, beta=0.7):
    """
    Krzyżowanie mieszające typu alfa i beta.
    """
    # Calculate gene-wise min and max
    min_genes = np.minimum(parent1.genes, parent2.genes)
    max_genes = np.maximum(parent1.genes, parent2.genes)
    
    # Calculate the difference (d_i)
    d_i = max_genes - min_genes
    
    # Calculate the expanded ranges
    lower_bound = min_genes - alpha * d_i
    upper_bound = max_genes + beta * d_i
    
    # Generate random values within the expanded ranges for both children
    child1_genes = np.random.uniform(lower_bound, upper_bound, size=parent1.genes.shape).astype(int)
    child2_genes = np.random.uniform(lower_bound, upper_bound, size=parent2.genes.shape).astype(int)
    return RealChromosome(len(parent1.genes)).set_genes(child1_genes), RealChromosome(len(parent2.genes)).set_genes(child2_genes)

def averaging_crossover(parent1, parent2):
    """
    Krzyżowanie uśredniające: każdy gen jest średnią genów rodziców.
    """
    child_genes = ((parent1.genes + parent2.genes) / 2).astype(int)
    return RealChromosome(len(parent1.genes)).set_genes(child_genes), RealChromosome(len(parent2.genes)).set_genes(child_genes)

