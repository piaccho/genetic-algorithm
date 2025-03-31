import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QStackedWidget, QApplication, QPushButton
from PyQt5.QtCore import QTimer
from form import ConfigForm, get_config_params_from_gui
from configuration import config
from genetic_algorithm import GeneticAlgorithm
from logger import log
from plotter import PlotWidget
import csv

class TimerWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Calculation Time: 0 seconds")
    
    def update_time(self, time):
        self.setText(f"Calculation Time: {time:.2f} seconds")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genetic Algorithm")
        self.setGeometry(100, 100, 800, 600)
        
        # Create stacked widget to switch between form and results view
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create form widget
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.config_form = ConfigForm()
        self.config_form.submit_button.clicked.connect(self.run_algorithm)
        self.form_layout.addWidget(self.config_form)
        
        # Create results widget
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        
        # Add timer widget
        self.timer_widget = TimerWidget()
        self.results_layout.addWidget(self.timer_widget)
        
        # Add plot widget
        self.plot_widget = PlotWidget()
        self.results_layout.addWidget(self.plot_widget)
        
        # Add back button to return to form
        self.back_button = QPushButton("Back to Configuration")
        self.back_button.clicked.connect(self.show_form)
        self.results_layout.addWidget(self.back_button)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.form_widget)
        self.stacked_widget.addWidget(self.results_widget)
        
        # Show form by default
        self.stacked_widget.setCurrentIndex(0)
        
        # Initialize GA and results
        self.ga = None
        self.results = []
        self.start_time = 0
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.current_epoch = 0

    def show_form(self):
        self.stacked_widget.setCurrentIndex(0)
        
    def show_results(self):
        self.stacked_widget.setCurrentIndex(1)

    def run_algorithm(self):
        # Switch to results view
        self.show_results()
        
        # Reset plot and timer
        self.timer_widget.setText("Calculation Time: 0 seconds")
        self.plot_widget.axes.clear()
        self.plot_widget.canvas.draw()
        
        # Get configuration from form
        config_params = get_config_params_from_gui(self.config_form)
        if config_params:
            config.update_from_dict(config_params)
        log(f"Configuration:\n{config}")
        
        # Create genetic algorithm instance
        self.ga = GeneticAlgorithm(config)
        
        # Initialize variables
        self.results = []
        self.current_epoch = 0
        self.start_time = time.time()
        
        # Start the timer for updates
        self.update_timer.start(100)  # Update every 100ms
        
        # Process events to update UI before starting algorithm
        QApplication.processEvents()
        
        # Run algorithm in batches to keep UI responsive
        self.run_next_epoch()
        
    def run_next_epoch(self):
        if self.current_epoch < config.epochs_num:
            # Run a single iteration
            self.ga.iteration(self.current_epoch)
            self.current_epoch += 1
            
            # Update display
            self.update_display()
            
            # Schedule next iteration
            QTimer.singleShot(1, self.run_next_epoch)
        else:
            # Algorithm completed
            self.update_timer.stop()
            elapsed_time = time.time() - self.start_time
            log(f"Algorithm completed in {elapsed_time:.2f} seconds")
            
            # Save results to CSV
            self.save_results_to_csv()
    
    def update_display(self):
        # Update timer
        elapsed_time = time.time() - self.start_time
        self.timer_widget.update_time(elapsed_time)
        
        # Update plot with current progress data
        if hasattr(self.ga, 'progress_data') and self.ga.progress_data:
            self.plot_widget.update_plot(self.ga.progress_data)
        
        # Process UI events
        QApplication.processEvents()
    
    def save_results_to_csv(self):
        # Zapis do pliku CSV z nagłówkami
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Generate and write headers
            headers = ["Epoch", "Population Size", "Current Best Fitness"]
            
            # Add headers for current epoch's best solution variables
            for i in range(config.num_variables):
                headers.append(f"X{i+1}")
                
            headers.append("Best Fitness All Time")
            
            # Add headers for best solution variables
            for i in range(config.num_variables):
                headers.append(f"Best X{i+1}")
                
            writer.writerow(headers)
            
            # Write the actual data
            for result in self.ga.progress_data:
                writer.writerow(result)

