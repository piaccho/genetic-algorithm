import numpy as np
from individual import Individual
from chromosome import Chromosome
from selection_methods import select_best, roulette_wheel_selection, tournament_selection
from cross_methods import single_point_crossover, two_point_crossover, uniform_crossover, granular_crossover
from mutation import single_point_mutation, two_point_mutation, boundary_mutation
from inversion import inversion

class Population:
    def __init__(self, size, chromosome_length, fitness_function, num_variables, begin_range, end_range):
        self.individuals = [
            Individual(
                chromosome=Chromosome(chromosome_length)
            ) for _ in range(size)
        ]
        self.fitness_function = fitness_function
        self.num_variables = num_variables
        self.begin_range = begin_range
        self.end_range = end_range

    def evaluate_fitness(self):
        # Obliczenie fitnes dla każdego osobnika w populacji
        for individual in self.individuals:
            individual.calculate_fitness(
                lambda: self.fitness_function(
                    individual.decode_chromosome(self.num_variables, self.begin_range, self.end_range)
                )
            )

    def selection(self, method='tournament', num_to_select=None, tournament_size=3):
        if method == 'best':
            self.individuals = select_best(self.individuals, num_to_select or len(self.individuals) // 2)
        elif method == 'roulette':
            self.individuals = roulette_wheel_selection(self.individuals, num_to_select or len(self.individuals) // 2)
        elif method == 'tournament':
            self.individuals = tournament_selection(self.individuals, num_to_select or len(self.individuals) // 2, tournament_size)

    def crossover(self, method='uniform', cross_probability=0.8):
        new_population = []
        for _ in range(len(self.individuals) // 2):
            if np.random.rand() < cross_probability:
                parent1, parent2 = np.random.choice(self.individuals, 2, replace=False)
                if method == 'single_point':
                    child1, child2 = single_point_crossover(parent1.chromosome, parent2.chromosome)
                elif method == 'two_point':
                    child1, child2 = two_point_crossover(parent1.chromosome, parent2.chromosome)
                elif method == 'uniform':
                    child1, child2 = uniform_crossover(parent1.chromosome, parent2.chromosome)
                elif method == 'granular':
                    child1, child2 = granular_crossover(parent1.chromosome, parent2.chromosome)
                new_population.extend([Individual(child1), Individual(child2)])
        self.individuals.extend(new_population)
        
    def mutate(self, method='single_point', mutation_probability=0.01):
        for individual in self.individuals:
            if np.random.rand() < mutation_probability:
                if method == 'single_point':
                    single_point_mutation(individual.chromosome)
                elif method == 'two_point':
                    two_point_mutation(individual.chromosome)
                elif method == 'boundary':
                    boundary_mutation(individual.chromosome)
    
    def apply_inversion(self, inversion_probability=0.01):
        for individual in self.individuals:
            if np.random.rand() < inversion_probability:
                inversion(individual.chromosome)