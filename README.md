# Introduction

The aim of the project is to implement a genetic algorithm for optimizing multi-variable functions. The project should be implemented in Python programming language.

# Project Assumptions

1. Implementation of a genetic algorithm for function maximization and minimization problems.
2. Ability to configure the number of variables (e.g., 5, 10, 20, 27).

# Implementation Elements

- Binary representation of chromosome and accuracy configuration.
- Population size configuration.
- Number of epochs configuration.
- Selection methods: best selection, roulette wheel, tournament.
- Crossover: single-point, two-point, uniform, granular.
- Mutations: boundary, single-point, and two-point.
- Inversion operator and elitist strategy.

# Selection of Test Functions

The multi-variable function that the genetic algorithm will optimize is the Hyperellipsoid function.

- Formula in LaTeX:

$$
f(x)=\sum_{i=0}^{N-1} \sum_{j=0}^{i} x_j^2
$$

- Suggested search range: `[-65.536, 65.536]`
- Global minimum: `(0.0, [0.0, 0.0])`

# Application and Visualization

1. Graphical user interface.
2. Ability to configure algorithm parameters through the GUI.
3. Display of computation time.
4. Generation of function value graphs across iterations.
5. Saving results to a file/database.