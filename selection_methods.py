import numpy as np

def select_best(population, num_to_select):
    """
    Select the best individuals based on their fitness scores.
    """
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    return sorted_population[:num_to_select]

def roulette_wheel_selection(population, num_to_select):
    """
    Roulette wheel selection method.
    Probability of selection is proportional to the fitness.
    """
    max_fitness_sum = sum(ind.fitness for ind in population)
    selection_probs = [ind.fitness / max_fitness_sum for ind in population]
    
    selected_individuals = np.random.choice(population, num_to_select, replace=False, p=selection_probs)
    return list(selected_individuals)

def tournament_selection(population, num_to_select, tournament_size):
    """
    Tournament selection method.
    Randomly picks 'tournament_size' individuals, and selects the best out of these to enter the next generation.
    Repeats until 'num_to_select' individuals are selected.
    """
    selected_individuals = []
    for _ in range(num_to_select):
        tournament_participants = np.random.choice(population, tournament_size, replace=False)
        winner = max(tournament_participants, key=lambda ind: ind.fitness)
        selected_individuals.append(winner)
    return selected_individuals