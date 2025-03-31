from population import Population
from fitness_functions import choose_fitness_function
from logger import log
import math

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.fitness_function = choose_fitness_function(config.fitness_function)
        self.population = Population(config.population_size,
                                     self.compute_chromosome_length(),
                                     self.fitness_function,
                                     config.num_variables,
                                     config.lower_bound,
                                     config.upper_bound)
        self.optimum = float('inf') if not config.maximization else float('-inf')
        self.optimum_variables = None
        self.progress_data = []

    def compute_chromosome_length(self):
        """Compute chromosome length based on number of variables and precision required."""
        return self.config.num_variables * math.ceil(math.log2((self.config.upper_bound - self.config.lower_bound) / self.config.precision))

    def run(self):
        """Run the genetic algorithm process for a set number of epochs."""
        # Clear any previous progress data
        self.progress_data = []
        
        for epoch in range(self.config.epochs_num):
            self.iteration(epoch)
        
        log(f"Found optimum: [{self.optimum}, {self.optimum_variables}]")
        
        # Return the progress data for all epochs
        return self.progress_data

    def iteration(self, epoch):
        """Execute a single iteration (epoch) of the genetic algorithm."""
        self.evaluate_fitness()
        self.report(epoch)
        self.selection()
        self.crossover()
        self.mutate()
        self.inversion()
        
    def evaluate_fitness(self):
        """Evaluate the fitness of each individual in the population."""
        self.population.evaluate_fitness()
    
    def report(self, epoch):
        """Report the results of the current epoch and save progress data."""
        best_individual = self.get_best()
        current_best_fitness = best_individual.fitness
        
        # Update the optimum if this epoch's best is better
        if self.config.maximization:
            if current_best_fitness > self.optimum:
                self.optimum = current_best_fitness
                self.optimum_variables = best_individual.decode_chromosome(self.config.num_variables, self.config.lower_bound, self.config.upper_bound)
        else:
            if current_best_fitness < self.optimum:
                self.optimum = current_best_fitness
                self.optimum_variables = best_individual.decode_chromosome(self.config.num_variables, self.config.lower_bound, self.config.upper_bound)
        
        # Get current best variables
        current_best_variables = best_individual.decode_chromosome(self.config.num_variables, self.config.lower_bound, self.config.upper_bound)
        
        # Create epoch data row:
        # [epoch_number, population_size, current_best_fitness, x1, x2, ..., best_fitness_all_time]
        epoch_data = [epoch + 1, len(self.population.individuals), current_best_fitness, *current_best_variables, self.optimum, *self.optimum_variables]
        
        # Store the data for this epoch
        self.progress_data.append(epoch_data)
        
        log(f"Epoch {epoch + 1}\tPopulation: {len(self.population.individuals)}\tBest Fitness: {current_best_fitness}")
    
    def get_best(self):
        """Returns the best individual from the population."""
        return max(self.population.individuals, key=lambda ind: ind.fitness) if self.config.maximization else min(self.population.individuals, key=lambda ind: ind.fitness)
    
    def selection(self):
        """Perform selection process as per the method defined in configuration."""
        self.population.selection(self.config.selection_method, self.config.select_best_amount, self.config.select_tournament_size, self.config.maximization)
    
    def crossover(self):
        """Perform crossover across the population members, based on probability."""
        self.population.crossover(self.config.crossover_method, self.config.crossover_probability)
    
    def mutate(self):
        """Mutate the population members, based on probability."""
        self.population.mutate(self.config.mutation_method, self.config.mutation_probability)
    
    def inversion(self):
        """Apply inversion operation to the population members, based on probability."""
        self.population.apply_inversion(self.config.inversion_probability)
