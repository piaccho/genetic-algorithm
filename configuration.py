class GeneticAlgorithmConfig:
    def __init__(self):
        
        # Określenie podstawowych ustawień algorytmu
        self.fitness_function = 'hyperellipsoid'  # 'hyperellipsoid' lub 'rosenbrock'
        self.lower_bound = -65.536
        self.upper_bound = 65.536
        self.precision = 0.001
        self.num_variables = 2
        self.population_size = 50
        self.epochs_num = 100
        self.elite_strategy_amount = 2

        # Prawdopodobieństwa dla różnych operacji ewolucyjnych
        self.crossover_probability = 0.8
        self.mutation_probability = 0.03
        self.inversion_probability = 0.1

        # Metody selekcji, krzyżowania i mutacji
        self.selection_method = 'tournament'  # 'roulette', 'tournament' lub 'best'
        self.select_best_amount = 10 
        self.select_tournament_size = 5  # Używany tylko gdy selection_method jest 'tournament'

        self.crossover_method = 'single_point'  # 'single_point', 'two_point', 'uniform', 'granular'
        self.mutation_method = 'single_point'  # 'single_point', 'two_point', 'boundary'

        # Czy algorytm ma maksymalizować (True) czy minimalizować (False) funkcje fitness
        self.maximization = False
        
    def update_from_dict(self, params):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)
    
    def __str__(self):
        """
        String representation of configurations for easy debugging and logging.
        """
        return "\n".join(f"\t{key}: {value}" for key, value in self.__dict__.items())
      
config = GeneticAlgorithmConfig()