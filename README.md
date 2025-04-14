# Genetic Algorithm

This project implements a genetic algorithm to solve optimization problems involving multi-variable functions. The algorithm is designed to be highly configurable, allowing users to adjust parameters such as population size, number of epochs, selection methods, crossover techniques, and mutation strategies. A graphical user interface (GUI) is provided to facilitate interaction and visualization of the algorithm's performance.

## Setup

To set up the project, ensure you have Python installed on your system. Follow these steps:

1. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

2. Run the application using:

```bash
python app.py
```

This will start the GUI application for genetic algorithm and allow you to interact with its features.

## Introduction

The aim of the project is to implement a genetic algorithm for optimizing multi-variable functions. The project should be implemented in Python programming language.

## Project Assumptions

1. Implementation of a genetic algorithm for function maximization and minimization problems.
2. Ability to configure the number of variables (e.g., 5, 10, 20, 27).

## Implementation Elements

- Binary representation of chromosome and accuracy configuration.
- Population size configuration.
- Number of epochs configuration.
- Selection methods: best selection, roulette wheel, tournament.
- Crossover: single-point, two-point, uniform, granular.
- Mutations: boundary, single-point, and two-point.
- Inversion operator and elitist strategy.

## Selection of Test Functions

The multi-variable function that the genetic algorithm will optimize is the Hyperellipsoid function.

- Formula in LaTeX:

$$
f(x)=\sum_{i=0}^{N-1} \sum_{j=0}^{i} x_j^2
$$

- Suggested search range: `[-65.536, 65.536]`
- Global minimum: `(0.0, [0.0, 0.0])`

## Application and Visualization

1. Graphical user interface.
2. Ability to configure algorithm parameters through the GUI.
3. Display of computation time.
4. Generation of function value graphs across iterations.
5. Saving results to a file/database.