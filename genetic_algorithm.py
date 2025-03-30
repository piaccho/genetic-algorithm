from population import Population
from fitness_functions import hyperellipsoid_function, rosenbrock_function

class GeneticAlgorithm:
    def __init__(self, fitness_function, num_variables, population_size, chromosome_length, num_generations,
                 crossover_probability, mutation_probability, inversion_probability, selection_method, 
                 crossover_method, mutation_method):
        self.population = Population(population_size, chromosome_length, fitness_function, num_variables,
                                     -100, 100)  # Zakres do zdefiniowania lepiej w zależności od funkcji fitness
        self.num_generations = num_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.inversion_probability = inversion_probability
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        
    def run(self):
        for generation in range(self.num_generations):
            print(f"Generation {generation + 1}")
            self.population.evaluate_fitness()
            self.population.selection(method=self.selection_method)
            self.population.crossover(method=self.crossover_method, cross_probability=self.crossover_probability)
            self.population.mutate(method=self.mutation_method, mutation_probability=self.mutation_probability)
            self.population.apply_inversion(self.inversion_probability)
            self.report_best()
            
    def report_best(self):
        best_individual = max(self.population.individuals, key=lambda ind: ind.fitness)
        print(f"Best Individual Fitness: {best_individual.fitness}")

# Example usage
if __name__ == "__main__":
    ga = GeneticAlgorithm(
        fitness_function=hyperellipsoid_function,
        num_variables=5,
        population_size=100,
        chromosome_length=50,  # length should be enough to encode the range adequately
        num_generations=50,
        crossover_probability=0.8,
        mutation_probability=0.01,
        inversion_probability=0.01,
        selection_method='tournament',
        crossover_method='uniform',
        mutation_method='single_point'
    )
    ga.run()