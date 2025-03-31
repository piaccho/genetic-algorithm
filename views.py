import time
import os
import subprocess
import platform
from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                            QStackedWidget, QApplication, QPushButton, QFrame, QGridLayout, 
                            QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from form import ConfigForm, get_config_params_from_gui
from configuration import config
from genetic_algorithm import GeneticAlgorithm
from logger import log
from plotter import PlotWidget
import csv

class StyledLabel(QLabel):
    def __init__(self, text="", parent=None, bold=False, font_size=12, align=Qt.AlignLeft):
        super().__init__(text, parent)
        font = QFont()
        if bold:
            font.setBold(True)
        font.setPointSize(font_size)
        self.setFont(font)
        self.setAlignment(align)

class TimerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)
        
        layout = QVBoxLayout(self)
        
        # Title for the timer
        self.timer_title = StyledLabel("Computation Time", self, bold=True, font_size=14, align=Qt.AlignCenter)
        layout.addWidget(self.timer_title)
        
        # Timer value
        self.timer_value = StyledLabel("0.00 seconds", self, bold=True, font_size=16, align=Qt.AlignCenter)
        layout.addWidget(self.timer_value)
        
        # Set a maximum width to make it stand out
        self.setMaximumWidth(300)
    
    def update_time(self, time):
        self.timer_value.setText(f"{time:.2f} seconds")

class VariablesWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)
        
        self.layout = QVBoxLayout(self)
        
        # Title for the variables
        self.title = StyledLabel("Current Best Solution", self, bold=True, font_size=14, align=Qt.AlignCenter)
        self.layout.addWidget(self.title)
        
        # Grid for variables and fitness
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        
        # Initial label
        self.grid.addWidget(StyledLabel("No data yet", self), 0, 0)
        
        # Set a preferred width
        self.setMinimumWidth(250)
    
    def update_variables(self, fitness, variables):
        """Update the displayed variables and fitness value"""
        # Clear current grid
        for i in reversed(range(self.grid.count())): 
            self.grid.itemAt(i).widget().setParent(None)
            
        # Add fitness value
        self.grid.addWidget(StyledLabel("Fitness:", self, bold=True), 0, 0)
        self.grid.addWidget(StyledLabel(f"{fitness:.6f}", self), 0, 1)
        
        # Add variables
        for i, var in enumerate(variables):
            self.grid.addWidget(StyledLabel(f"X{i+1}:", self, bold=True), i+1, 0)
            self.grid.addWidget(StyledLabel(f"{var:.6f}", self), i+1, 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genetic Algorithm - Configuration")
        self.setGeometry(100, 100, 700, 700)
        
        # Create stacked widget to switch between form and results view
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create form widget with title
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)

        # Add configuration form
        self.config_form = ConfigForm()
        self.config_form.submit_button.clicked.connect(self.run_algorithm)
        self.form_layout.addWidget(self.config_form)
        
        # Create results widget with title
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        
        # Create info widgets container (timer and variables)
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        
        # Add variables widget (left side)
        self.variables_widget = VariablesWidget()
        info_layout.addWidget(self.variables_widget)
        
        # Add timer widget (right side)
        self.timer_widget = TimerWidget()
        info_layout.addWidget(self.timer_widget)
        
        # Add info container to results layout
        self.results_layout.addWidget(info_container)
        
        # Add plot widget
        self.plot_widget = PlotWidget()
        self.results_layout.addWidget(self.plot_widget)
        
        # Add status label for CSV saving
        self.status_label = StyledLabel("", self, align=Qt.AlignCenter)
        self.results_layout.addWidget(self.status_label)
        
        # Add buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        
        # Add back button to return to form
        self.back_button = QPushButton("Back to Configuration")
        self.back_button.clicked.connect(self.show_form)
        buttons_layout.addWidget(self.back_button)
        
        # Add open in explorer button
        self.open_file_button = QPushButton("Open Results File")
        self.open_file_button.clicked.connect(self.open_results_file)
        buttons_layout.addWidget(self.open_file_button)
        
        # Add buttons container to results layout
        self.results_layout.addWidget(buttons_container)
        
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
        
        # Results file path
        self.results_file_path = os.path.abspath('results.csv')


    def show_form(self):
        self.setWindowTitle("Genetic Algorithm - Configuration")
        self.stacked_widget.setCurrentIndex(0)
        
    def show_results(self):
        self.setWindowTitle("Genetic Algorithm - Execution")
        self.stacked_widget.setCurrentIndex(1)

    def run_algorithm(self):
        # Switch to results view
        self.show_results()
        
        # Reset plot, timer and status
        self.timer_widget.update_time(0)
        self.plot_widget.axes.clear()
        self.plot_widget.canvas.draw()
        self.status_label.setText("")
        
        # Disable the open file button while running
        self.open_file_button.setEnabled(False)
        
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
            
            # Show completion message
            self.status_label.setStyleSheet("color: #5eead4; font-weight: bold; font-size: 14px; padding: 10px;")
            self.status_label.setText("✓ Optimization complete! Results saved to file.")
            
            # Enable the open file button now that algorithm is complete
            self.open_file_button.setEnabled(True)
    
    def open_results_file(self):
        """Open the results CSV file in the default file explorer"""
        if not os.path.exists(self.results_file_path):
            QMessageBox.warning(self, "File Not Found", 
                              "Results file not found. Please run the algorithm first.")
            return
            
        try:
            # Cross-platform way to open files in their default application
            if platform.system() == "Windows":
                os.startfile(self.results_file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.results_file_path])
            else:  # Linux
                subprocess.call(["xdg-open", self.results_file_path])
        except Exception as e:
            QMessageBox.warning(self, "Error Opening File", 
                              f"Could not open the file: {str(e)}")
    
    
    def update_display(self):
        # Update timer
        elapsed_time = time.time() - self.start_time
        self.timer_widget.update_time(elapsed_time)
        
        # Update variables display if we have data
        if hasattr(self.ga, 'progress_data') and self.ga.progress_data:
            latest_data = self.ga.progress_data[-1]
            current_fitness = latest_data[2]  # Current best fitness
            
            num_vars = config.num_variables
            variables = latest_data[3:3+num_vars]  # Extract variables from data
            
            # Update the variables widget
            self.variables_widget.update_variables(current_fitness, variables)
        
        # Update plot with current progress data
        if hasattr(self.ga, 'progress_data') and self.ga.progress_data:
            self.plot_widget.update_plot(self.ga.progress_data)
        
        # Process UI events
        QApplication.processEvents()
    
    def save_results_to_csv(self):
        # Ensure the results directory exists
        results_dir = os.path.abspath('./results')
        os.makedirs(results_dir, exist_ok=True)
        
        # Generate a timestamped filename
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"results-{timestamp}.csv"
        
        self.results_file_path = os.path.join(results_dir, filename)
        
        # Save to CSV file with headers
        with open(self.results_file_path, 'w', newline='') as file:
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
                
        # Optionally show a popup message
        QMessageBox.information(self, "Export Complete", 
                              "Results have been successfully saved to results.csv")