import numpy as np
from chromosome import Chromosome

def single_point_crossover(parent1, parent2):
    """
    Single-point crossover between two chromosomes.
    """
    crossover_point = np.random.randint(1, len(parent1.genes) - 1)
    child1_genes = np.concatenate((parent1.genes[:crossover_point], parent2.genes[crossover_point:]))
    child2_genes = np.concatenate((parent2.genes[:crossover_point], parent1.genes[crossover_point:]))
    return Chromosome(len(parent1.genes)).set_genes(child1_genes), Chromosome(len(parent2.genes)).set_genes(child2_genes)

def two_point_crossover(parent1, parent2):
    """
    Two-point crossover between two chromosomes.
    """
    points = np.sort(np.random.choice(range(1, len(parent1.genes) - 1), 2, replace=False))
    child1_genes = np.concatenate((parent1.genes[:points[0]], parent2.genes[points[0]:points[1]], parent1.genes[points[1]:]))
    child2_genes = np.concatenate((parent2.genes[:points[0]], parent1.genes[points[0]:points[1]], parent2.genes[points[1]:]))
    return Chromosome(len(parent1.genes)).set_genes(child1_genes), Chromosome(len(parent2.genes)).set_genes(child2_genes)

def uniform_crossover(parent1, parent2):
    """
    Uniform crossover, where each gene is randomly chosen from one of the parents.
    """
    mask = np.random.rand(len(parent1.genes)) > 0.5
    child1_genes = np.where(mask, parent1.genes, parent2.genes)
    child2_genes = np.where(mask, parent2.genes, parent1.genes)
    return Chromosome(len(parent1.genes)).set_genes(child1_genes), Chromosome(len(parent2.genes)).set_genes(child2_genes)

def granular_crossover(parent1, parent2, granularity=5):
    """
    Granular crossover, where blocks of genes are chosen from parents.
    Each block's length is determined by granularity.
    """
    num_blocks = len(parent1.genes) // granularity
    mask = np.random.rand(num_blocks) > 0.5
    child1_genes = []
    child2_genes = []
    for i in range(num_blocks):
        start_idx = i * granularity
        end_idx = start_idx + granularity
        if mask[i]:
            child1_genes.extend(parent1.genes[start_idx:end_idx])
            child2_genes.extend(parent2.genes[start_idx:end_idx])
        else:
            child1_genes.extend(parent2.genes[start_idx:end_idx])
            child2_genes.extend(parent1.genes[start_idx:end_idx])
    return Chromosome(len(parent1.genes)).set_genes(np.array(child1_genes)), Chromosome(len(parent2.genes)).set_genes(np.array(child2_genes))