import numpy as np

def select_best(population, num_to_select, maximization=False):
    """
    Select the best individuals based on their fitness scores.
    """
    # log(f"Performing best selection: selecting {num_to_select} from population of {len(population)}")
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=maximization)
    selected = sorted_population[:num_to_select]
    # log(f"Selected {len(selected)} best individuals. Top fitness: {selected[0].fitness if selected else 'N/A'}")
    return selected

def roulette_wheel_selection(population, num_to_select, maximization=False):
    """
    Roulette wheel selection method.
    Probability of selection is proportional to the fitness.
    """
    # For minimization problems, we need to transform the fitness values
    # since lower values are better but we need higher probabilities
    if not maximization:
        max_fitness = max(ind.fitness for ind in population)
        min_fitness = min(ind.fitness for ind in population)
        
        # If all fitness values are the same, use equal probabilities
        if max_fitness == min_fitness:
            selection_probs = [1.0/len(population) for _ in population]
        else:
            # Transform fitness: higher values for lower fitness
            # Adding a small epsilon to avoid issues with identical fitness values
            epsilon = 1e-10
            transformed_fitness = [max_fitness - ind.fitness + epsilon for ind in population]
            total_transformed = sum(transformed_fitness)
            selection_probs = [tf/total_transformed for tf in transformed_fitness]
    else:
        # For maximization, higher fitness should get higher probability
        total_fitness = sum(ind.fitness for ind in population)
        
        # Handle the case where all fitness values might be zero
        if total_fitness == 0:
            selection_probs = [1.0/len(population) for _ in population]
        else:
            selection_probs = [ind.fitness/total_fitness for ind in population]
    
    # Perform selection
    selected_individuals = np.random.choice(population, num_to_select, replace=False, p=selection_probs)
    
    return list(selected_individuals)

def tournament_selection(population, num_to_select, tournament_size, maximization=False):
    """
    Tournament selection method.
    Divides population into k-element subgroups (tournament_size) and selects the best individual from each subgroup.
    """
    # Ensure tournament size doesn't exceed population size
    actual_tournament_size = min(tournament_size, len(population))
    
    # Check if we have enough individuals to select
    if num_to_select > len(population):
        raise ValueError("num_to_select cannot be greater than population size")
    
    selected_individuals = []
    population_copy = population.copy()  # Work on a copy to preserve original population
    
    while len(selected_individuals) < num_to_select and population_copy:
        # Randomly select tournament participants
        if len(population_copy) <= actual_tournament_size:
            tournament_participants = population_copy
        else:
            tournament_participants = np.random.choice(population_copy, actual_tournament_size, replace=False)
            
        # Find the best individual in the tournament
        if maximization:
            winner = max(tournament_participants, key=lambda ind: ind.fitness)
        else:
            winner = min(tournament_participants, key=lambda ind: ind.fitness)
        
        selected_individuals.append(winner)
        population_copy.remove(winner)
    
    return selected_individuals
  
