import numpy as np

def inversion(chromosome):
    """
    Performs inversion mutation on a chromosome. It selects two random points, 
    slicing the chromosome into three parts, then reverses the middle part and reassembles the chromosome.
    """
    length = len(chromosome.genes)
    if length < 3:
        return  # Too short to invert meaningfully
    
    # Select two unique points for slicing the chromosome, ensuring they are not on the boundary.
    point1, point2 = sorted(np.random.choice(range(1, length - 1), 2, replace=False))
    
    # Break chromosome into three parts
    left = chromosome.genes[:point1]
    middle = chromosome.genes[point1:point2]
    right = chromosome.genes[point2:]
    
    # Reverse the middle section
    middle = middle[::-1]
    
    # Reassemble the chromosome
    chromosome.set_genes(np.concatenate([left, middle, right]))