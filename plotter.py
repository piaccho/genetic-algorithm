from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Create the figure and canvas for plotting
        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor='#1e2433')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Initialize the plot
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Fitness Evolution', color='#e0e7ff')
        self.axes.set_xlabel('Generation', color='#e0e7ff')
        self.axes.set_ylabel('Fitness', color='#e0e7ff')
        self.axes.grid(True, color='#3d5a80', linestyle='-', alpha=0.3)
        self.axes.set_facecolor('#263041')
        self.axes.tick_params(colors='#e0e7ff')
        self.axes.spines['bottom'].set_color('#3d5a80')
        self.axes.spines['top'].set_color('#3d5a80') 
        self.axes.spines['right'].set_color('#3d5a80')
        self.axes.spines['left'].set_color('#3d5a80')

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
        self.axes.plot(epochs, current_fitness, '#56cfe1', linewidth=2, marker='o', 
                      markersize=4, label='Current Best Fitness')
        self.axes.plot(epochs, best_fitness, '#ff66b3', linewidth=2, marker='s', 
                      markersize=4, label='All-time Best Fitness')

        # Add labels and legend
        self.axes.set_title('Fitness Evolution', color='#e0e7ff')
        self.axes.set_xlabel('Generation', color='#e0e7ff')
        self.axes.set_ylabel('Fitness', color='#e0e7ff')
        self.axes.legend(loc='best', facecolor='#263041', edgecolor='#3d5a80', labelcolor='#e0e7ff')
        self.axes.grid(True, color='#3d5a80', linestyle='-', alpha=0.3)
        self.axes.tick_params(colors='#e0e7ff')
        
        # Refresh the canvas
        self.canvas.draw()
        
    def save_plot(self, filepath):
        """
        Save the current plot to an image file.
        
        Args:
            filepath: Path where to save the image
        """
        self.figure.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=self.figure.get_facecolor())
        return True