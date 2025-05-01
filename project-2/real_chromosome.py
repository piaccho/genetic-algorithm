import numpy as np

class RealChromosome:
    # Inicjalizacja Chromosomu rzeczywistego
    def __init__(self, length):
        # Losowe stworzenie chromosomu z liczbami całkowitymi w zakresie od 0 do 10
        self.genes = np.random.randint(0, 11, length)

    def __str__(self):
        # Reprezentacja tekstowa chromosomu jako ciąg liczb całkowitych
        return ', '.join(str(gene) for gene in self.genes)

    def set_genes(self, gene_array):
        # Ustawianie genów chromosomu
        self.genes = gene_array
        return self

    def mutate(self):
        # Mutacja: zmiana jednego losowego genu na nową wartość w zakresie od 0 do 10
        mutation_point = np.random.randint(0, len(self.genes))
        self.genes[mutation_point] = np.random.randint(0, 11)

    def crossover(self, other, crossover_point=None):
        # Krzyżowanie jednopunktowe
        if crossover_point is None:
            # Losowy punkt krzyżowania, jeśli nie został podany
            crossover_point = np.random.randint(1, len(self.genes))
        # Tworzenie dwóch dzieci poprzez wymianę genów w punkcie krzyżowania
        child1_gen = np.append(self.genes[:crossover_point], other.genes[crossover_point:])
        child2_gen = np.append(other.genes[:crossover_point], self.genes[crossover_point:])
        return RealChromosome(len(self.genes)).set_genes(child1_gen), RealChromosome(len(other.genes)).set_genes(child2_gen)
