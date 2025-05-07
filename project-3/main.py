#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/
import logging
import pygad
import numpy as np
import matplotlib.pyplot as plt
import benchmark_functions as bf
import json
from datetime import datetime
import os
import shutil

# Domyślna konfiguracja
DEFAULT_CONFIG = {
    'selection': 'tournament',
    'crossover': 'single_point',
    'mutation': 'random',
    'gene_type': 'int'
}

# Konfiguracje do przetestowania
TEST_CONFIGS = [
    # Testy dla int
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'int'},  # default
    {'selection': 'rws', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'int'},
    {'selection': 'random', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'int'},
    {'selection': 'tournament', 'crossover': 'two_points', 'mutation': 'random', 'gene_type': 'int'},
    {'selection': 'tournament', 'crossover': 'uniform', 'mutation': 'random', 'gene_type': 'int'},
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'swap', 'gene_type': 'int'},
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'int'},
    
    # Testy dla float
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'float'},  # default
    {'selection': 'rws', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'float'},
    {'selection': 'random', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'float'},
    {'selection': 'tournament', 'crossover': 'two_points', 'mutation': 'random', 'gene_type': 'float'},
    {'selection': 'tournament', 'crossover': 'uniform', 'mutation': 'random', 'gene_type': 'float'},
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'swap', 'gene_type': 'float'},
    {'selection': 'tournament', 'crossover': 'single_point', 'mutation': 'random', 'gene_type': 'float'},
]

# Konfiguracja algorytmu genetycznego
num_genes = 2
func = bf.Hyperellipsoid(n_dimensions=num_genes)

# Parametry algorytmu
num_generations = 100
sol_per_pop = 100
num_parents_mating = 50
mutation_num_genes = 1
mutation_probability = 0.1
keep_elitism = 1
K_tournament = 5

def get_config_dir(config, test_id):
    """Tworzy nazwę katalogu dla danej konfiguracji"""
    gene_type = config['gene_type']
    selection = config['selection']
    crossover = config['crossover']
    mutation = config['mutation']
    return f"results/{gene_type}/{test_id}_{selection}_{crossover}_{mutation}"

def setup_logger(config, test_id):
    """Konfiguruje logger z odpowiednią ścieżką do pliku"""
    config_dir = get_config_dir(config, test_id)
    os.makedirs(config_dir, exist_ok=True)
    
    logger = logging.getLogger(config_dir)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(f'{config_dir}/log.txt', 'a+', 'utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s - %(pathname)s:%(lineno)d', 
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    return logger

def get_gene_type(gene_type_str):
    """Konwertuje string na typ Pythona"""
    if gene_type_str == 'int':
        return int
    elif gene_type_str == 'float':
        return float
    else:
        raise ValueError(f"Nieznany typ genu: {gene_type_str}")

def run_test(config, func, logger, test_id):
    """Uruchamia pojedynczy test z daną konfiguracją"""
    logger.info(f"\nRunning test with configuration: {config}")

    # Lista do przechowywania statystyk
    generations_stats = []
    
    # Konfiguracja zakresów
    lower_boundary, upper_boundary = func.suggested_bounds()
    init_range_low = lower_boundary[0]
    init_range_high = upper_boundary[0]
    
    # Funkcja fitness
    def fitness_func(ga_instance, solution, solution_idx):
        # Konwersja numpy.int64 na Python int/float
        solution = [float(x) for x in solution]
        fitness = func(solution)
        # Dla problemu minimalizacji, im mniejsza wartość tym lepsza
        return -fitness  # Zmiana znaku, bo PyGAD maksymalizuje funkcję fitness
    
    # Callback dla każdej generacji
    def on_generation(ga_instance):
        solution, solution_fitness, solution_idx = ga_instance.best_solution(
            pop_fitness=ga_instance.last_generation_fitness)
        
        tmp = [-x for x in ga_instance.last_generation_fitness]  # Odwracamy znak
        
        stats = {
            'generation': ga_instance.generations_completed,
            'best_fitness': -solution_fitness,  # Odwracamy znak
            'best_solution': solution.tolist(),
            'min': float(np.min(tmp)),
            'max': float(np.max(tmp)),
            'average': float(np.average(tmp)),
            'std': float(np.std(tmp)),
            'population': ga_instance.population.tolist() 
        }
        
        logger.info(f"Generation {stats['generation']}: Best = {stats['best_fitness']}")
        generations_stats.append(stats) 
    
    # Konfiguracja GA
    ga_instance = pygad.GA(
        num_generations=num_generations,
        sol_per_pop=sol_per_pop,
        num_parents_mating=num_parents_mating,
        num_genes=num_genes,
        fitness_func=fitness_func,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        mutation_num_genes=mutation_num_genes,
        mutation_probability=mutation_probability,
        parent_selection_type=config['selection'],
        crossover_type=config['crossover'],
        mutation_type=config['mutation'],
        gene_type=get_gene_type(config['gene_type']),
        keep_elitism=keep_elitism,
        K_tournament=K_tournament,
        random_mutation_max_val=1.0,
        random_mutation_min_val=-1.0,
        logger=logger,
        on_generation=on_generation,
        parallel_processing=['thread', 4]
    )
    
    # Uruchomienie algorytmu
    ga_instance.run()
    
    # Zbieranie wyników
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    
    results = {
        'config': config,
        'best_solution': solution.tolist(),
        'best_fitness': -solution_fitness,  # Odwracamy znak
        'generations': ga_instance.generations_completed,
        'fitness_history': [-x for x in ga_instance.best_solutions_fitness],  # Odwracamy znak
        'generations_stats': generations_stats
    }
    
    # Zapisywanie wyników
    config_dir = get_config_dir(config, test_id)
    os.makedirs(config_dir, exist_ok=True)  # Upewniamy się, że katalog istnieje
    
    # Wizualizacja - statystyki dla każdej generacji
    plt.figure(figsize=(12, 8))
    
    # Przygotowanie danych
    generations = range(1, num_generations + 1)
    best_values = [stats['best_fitness'] for stats in generations_stats]
    avg_values = [stats['average'] for stats in generations_stats]
    std_values = [stats['std'] for stats in generations_stats]

    # Wykres wartości najlepszych
    plt.subplot(2, 1, 1)
    plt.plot(generations, best_values, 'b-', label='Best Fitness')
    plt.title(f"Best Fitness Values - {config}")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend()
    
    # Wykres średniej i odchylenia standardowego
    plt.subplot(2, 1, 2)
    plt.plot(generations, avg_values, 'g-', label='Average Fitness')
    plt.fill_between(generations, 
                    [avg - std for avg, std in zip(avg_values, std_values)],
                    [avg + std for avg, std in zip(avg_values, std_values)],
                    alpha=0.2, color='g', label='±1 Std Dev')
    plt.title(f"Population Statistics - {config}")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"{config_dir}/statistics.png")
    plt.close()

    # Wykres populacji dla każdej generacji co 10 
    config_dir = get_config_dir(config, test_id)
    selected_generations = generations_stats[::10]
    num_plots = len(selected_generations)
    rows = int(np.ceil(np.sqrt(num_plots)))
    cols = int(np.ceil(num_plots / rows))
    
    plt.figure(figsize=(cols*4, rows*4))
    for i, stats in enumerate(selected_generations):
        plt.subplot(rows, cols, i+1)
        population = np.array(stats['population'])
        plt.scatter(population[:, 0], population[:, 1], alpha=0.5)
        plt.title(f"Generation {stats['generation']}")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f"{config_dir}/population_evolution.png")
    plt.close()
    
    # Zapisywanie wyników do JSON
    with open(f'{config_dir}/results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

def main():
    # Tworzenie głównego katalogu results
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.makedirs('results')
    os.makedirs('results/int', exist_ok=True)
    os.makedirs('results/float', exist_ok=True)
    
    # Inicjalizacja funkcji testowej
    func = bf.Hyperellipsoid(n_dimensions=num_genes)
    
    # Wyniki wszystkich testów
    all_results = []
    
    # Uruchomienie testów
    for i, config in enumerate(TEST_CONFIGS, 1):
        logger = setup_logger(config, i)
        results = run_test(config, func, logger, i)
        all_results.append(results)
        logger.handlers.clear()
    
    # Zapisywanie zbiorczych wyników
    with open(f'results/all_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()


