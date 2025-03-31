from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Create the figure and canvas for plotting
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Initialize the plot
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Fitness Over Generations')
        self.axes.set_xlabel('Generation')
        self.axes.set_ylabel('Fitness')
        self.axes.grid(True)

        # Variables to store previous plot data
        self.current_fitness_line = None
        self.best_fitness_line = None
    
    def update_plot(self, results):
        """
        Update the plot with new results data from the genetic algorithm.
        
        Args:
            results: List of results from each epoch [epoch, pop_size, current_fitness, x1, x2, ..., best_fitness]
        """
        if not results:
            return
            
        # Clear previous plot
        self.axes.clear()
        
        # Extract data from results
        epochs = [result[0] for result in results]
        current_fitness = [result[2] for result in results]  # Current best fitness is at index 2
        
        # The best fitness all-time is the last element in each result
        best_fitness = [result[-1] for result in results]
        
        # Plot the data
        self.axes.plot(epochs, current_fitness, 'b-', label='Current Best Fitness')
        self.axes.plot(epochs, best_fitness, 'r-', label='All-time Best Fitness')
        
        # Add labels and legend
        self.axes.set_title('Fitness Evolution')
        self.axes.set_xlabel('Generation')
        self.axes.set_ylabel('Fitness')
        self.axes.legend(loc='best')
        self.axes.grid(True)
        
        # Refresh the canvas
        self.canvas.draw()