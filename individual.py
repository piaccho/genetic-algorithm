class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None

    def calculate_fitness(self, fitness_function):
        # Policzenie wartości funkcji przystosowania (fitness) danego osobnika
        self.fitness = fitness_function()

    def decode_chromosome(self, num_variables, begin_range, end_range):
        # Dekodowanie chromosomu z postaci binarnej na wartości rzeczywiste
        segment_length = len(self.chromosome.genes) // num_variables
        variables = []
        
        for i in range(num_variables):
            # Dla każdej zmiennej, przekonwertuj odpowiedni segment genów do wartości rzeczywistej
            segment = self.chromosome.genes[i * segment_length:(i + 1) * segment_length]
            total = 0
            for gene in segment:
                total = total * 2 + int(gene)
            max_dec_value = 2 ** segment_length - 1
            scaled_value = begin_range + (total / max_dec_value) * (end_range - begin_range)
            variables.append(scaled_value)
        return variables  

    def __str__(self):
        # Tekstowa reprezentacja osobnika z wartością jego fitness
        return f"Individual(Chromosome: {self.chromosome}, Fitness: {self.fitness})"
      
    def __repr__(self):
        return self.__str__()