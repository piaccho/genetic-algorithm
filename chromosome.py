import numpy as np

class Chromosome:
    # Inicjalizacja Chromosomu z binarną reprezentacją
    def __init__(self, length):
        # Losowe stworzenie binarnej reprzentacji chromosomu (ciąg bitów)
        self.genes = np.random.randint(0, 2, length).astype(np.bool_)

    def __str__(self):
        # Reprezentacja tekstowa chromosomu jako ciąg '0' i '1'
        return ''.join(str(int(gene)) for gene in self.genes)

    @staticmethod
    def from_number(number, length):
        # Tworzenie chromosomu na podstawie liczby dziesiętnej (number)
        return Chromosome(length).set_genes(np.array(list(bin(number)[2:].zfill(length)), dtype=np.bool_))

    def set_genes(self, gene_array):
        # Ustawianie genów chromosomu
        self.genes = gene_array
        return self

    def mutate(self):
        # Mutacja: odwracanie jednego losowego bitu
        mutation_point = np.random.randint(0, len(self.genes))
        self.genes[mutation_point] = not self.genes[mutation_point]

    def crossover(self, other, crossover_point):
        # Krzyżowanie jednopunktowe
        child1_gen = np.append(self.genes[:crossover_point], other.genes[crossover_point:])
        child2_gen = np.append(other.genes[:crossover_point], self.genes[crossover_point:])
        return Chromosome(len(self.genes)).set_genes(child1_gen), Chromosome(len(other.genes)).set_genes(child2_gen)