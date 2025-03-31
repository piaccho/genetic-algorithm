import time
import os
import subprocess
import platform
from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                           QStackedWidget, QApplication, QPushButton, QFrame, QGridLayout, 
                           QMessageBox, QGroupBox, QScrollArea, QFormLayout)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from form import ConfigForm, get_config_params_from_gui
from configuration import config
from genetic_algorithm import GeneticAlgorithm
from logger import log
from plotter import PlotWidget
import csv

class ConfigDisplayWidget(QFrame):
    """Widget to display the current configuration parameters"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)
        
        self.layout = QVBoxLayout(self)
        
        # Title
        self.title = StyledLabel("Algorithm Parameters", self, bold=True, font_size=14, align=Qt.AlignCenter)
        self.layout.addWidget(self.title)
        
        # Scrollable area for parameters
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        
        # Parameter groups
        self.params_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.params_layout)
        
        # Add stretch to push content to the top
        self.scroll_layout.addStretch()
        
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        
        # Initial empty state
        self.params_layout.addWidget(StyledLabel("No parameters loaded", self))
    
    def update_config(self, config_params):
        """Update the displayed configuration parameters"""
        # Clear current parameters
        for i in reversed(range(self.params_layout.count())):
            item = self.params_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # Group parameters by category
        categories = {
            "Problem Definition": ["fitness_function", "lower_bound", "upper_bound", 
                                 "precision", "num_variables"],
            "Population Settings": ["population_size", "epochs_num", "elite_strategy_amount", 
                                  "maximization"],
            "Genetic Operations": ["crossover_probability", "mutation_probability", 
                                 "inversion_probability"],
            "Selection Method": ["selection_method", "select_best_amount", "select_tournament_size"],
            "Genetic Methods": ["crossover_method", "mutation_method"]
        }
        
        # Add each category with its parameters
        for category, param_keys in categories.items():
            group = QGroupBox(category)
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #3d5a80;
                    border-radius: 5px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #263041;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 3px;
                    color: #98c1d9;
                }
            """)
            
            form_layout = QFormLayout(group)
            
            for key in param_keys:
                if key in config_params:
                    value = config_params[key]
                    # Format the value for display
                    if isinstance(value, bool):
                        value = "Yes" if value else "No"
                    elif isinstance(value, float):
                        value = f"{value:.6f}" if abs(value) < 0.1 else f"{value:.4f}"
                    
                    # Format the key for display (convert snake_case to Title Case)
                    display_key = " ".join(word.capitalize() for word in key.split('_'))
                    form_layout.addRow(
                        StyledLabel(f"{display_key}:", bold=True),
                        StyledLabel(f"{value}")
                    )
            
            self.params_layout.addWidget(group)
            
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
        self.setGeometry(100, 100, 1000, 700)  # Wider window for two columns
        
        # Create stacked widget to switch between form and results view
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create form widget with title
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        
        # Add form title
        # self.form_title = StyledLabel("Algorithm Configuration", self, bold=True, font_size=20, align=Qt.AlignCenter)
        # self.form_title.setStyleSheet("color: #56cfe1; margin-bottom: 10px;")
        # self.form_layout.addWidget(self.form_title)

        # Add configuration form
        self.config_form = ConfigForm()
        self.config_form.submit_button.clicked.connect(self.run_algorithm)
        self.form_layout.addWidget(self.config_form)
        
        # Create results widget
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        
        # Add results title
        # self.results_title = StyledLabel("Algorithm Execution", self, bold=True, font_size=20, align=Qt.AlignCenter)
        # self.results_title.setStyleSheet("color: #56cfe1; margin-bottom: 10px;")
        # self.results_layout.addWidget(self.results_title)
        
        # Create horizontal layout for two columns
        columns_container = QWidget()
        columns_layout = QHBoxLayout(columns_container)
        
        # Create left column for plot and stats
        left_column = QVBoxLayout()
        
        # Info widgets in the left column (timer and variables)
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        
        # Add variables widget
        self.variables_widget = VariablesWidget()
        info_layout.addWidget(self.variables_widget)
        
        # Add timer widget
        self.timer_widget = TimerWidget()
        info_layout.addWidget(self.timer_widget)
        
        left_column.addWidget(info_container)
        
        # Add plot widget to left column
        self.plot_widget = PlotWidget()
        left_column.addWidget(self.plot_widget)
        
        # Create right column for config parameters
        right_column = QVBoxLayout()
        
        # Add config display widget
        self.config_display = ConfigDisplayWidget()
        right_column.addWidget(self.config_display)
        
        # Add columns to container
        columns_layout.addLayout(left_column, 2)  # 2:1 ratio (plot gets more space)
        columns_layout.addLayout(right_column, 1)
        
        # Add columns container to results layout
        self.results_layout.addWidget(columns_container)
        
        # Add status label for CSV saving
        self.status_label = StyledLabel("", self, align=Qt.AlignCenter)
        self.results_layout.addWidget(self.status_label)
        
        # Add buttons container at the bottom
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        
        # Add back button
        self.back_button = QPushButton("Back to configuration")
        self.back_button.clicked.connect(self.show_form)
        buttons_layout.addWidget(self.back_button)
        
        # Add open file button
        self.open_file_button = QPushButton("Open results file")
        self.open_file_button.clicked.connect(self.open_results_file)
        buttons_layout.addWidget(self.open_file_button)
        
        # Add open plot button (initially hidden)
        self.view_plot_button = QPushButton("Open plot image")
        self.view_plot_button.clicked.connect(self.open_plot_file)
        buttons_layout.addWidget(self.view_plot_button)
        
        
        # Add buttons to results layout
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
        self.results_file_path = None
        self.plot_file_path = None


    def show_form(self):
        self.setWindowTitle("Genetic Algorithm - Configuration")
        self.stacked_widget.setCurrentIndex(0)
        # Reset buttons
        self.open_file_button.setEnabled(True)
        self.view_plot_button.setEnabled(False)
        
        
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
        
        # Disable the buttons while running
        self.open_file_button.setEnabled(False)
        self.view_plot_button.setEnabled(False)
        
        # Get configuration from form
        config_params = get_config_params_from_gui(self.config_form)
        if config_params:
            config.update_from_dict(config_params)
        log(f"Configuration:\n{config}")
        
        # Update the config display with the current parameters
        self.config_display.update_config(config_params)
        
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
            
            # Ensure the results directory exists
            results_dir = os.path.abspath('./results')
            os.makedirs(results_dir, exist_ok=True)
            
            # Generate a timestamped filename
            timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
            
            # Save results to CSV
            csv_filename = f"results-{timestamp}.csv"
            self.results_file_path = os.path.join(results_dir, csv_filename)
            self.save_results_to_csv()
            
            # Save plot to image file
            plot_filename = f"plot-{timestamp}.png"
            self.plot_file_path = os.path.join(results_dir, plot_filename)
            self.plot_widget.save_plot(self.plot_file_path)
            
            # Show a popup message with the results
            self.show_popup_message(elapsed_time)
            
            # Show completion message
            self.status_label.setStyleSheet("color: #5eead4; font-weight: bold; font-size: 14px; padding: 10px;")
            self.status_label.setText("✓ Optimization complete! Results and plot saved to files.")
            
            # Enable buttons
            self.open_file_button.setEnabled(True)
            self.view_plot_button.setEnabled(True)
    
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
    
    def open_plot_file(self):
        """Open the saved plot image in the default image viewer"""
        if not self.plot_file_path or not os.path.exists(self.plot_file_path):
            QMessageBox.warning(self, "File Not Found", 
                            "Plot image file not found. Please run the algorithm first.")
            return
            
        try:
            # Cross-platform way to open files in their default application
            if platform.system() == "Windows":
                os.startfile(self.plot_file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.plot_file_path])
            else:  # Linux
                subprocess.call(["xdg-open", self.plot_file_path])
        except Exception as e:
            QMessageBox.warning(self, "Error Opening File", 
                            f"Could not open the plot image: {str(e)}")    

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
        """Save results to a CSV file with headers"""
        if not self.results_file_path:
            # Generate default path if none was set
            results_dir = os.path.abspath('./results')
            os.makedirs(results_dir, exist_ok=True)
            timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
            self.results_file_path = os.path.join(results_dir, f"results-{timestamp}.csv")
        
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
            
        return self.results_file_path
                
    def show_popup_message(self, elapsed_time):
        """Show a popup message with the results"""
        msg = f"Algorithm completed in {elapsed_time:.2f} seconds.\n\nBest solution:\n"
        msg += f"    Fitness:\t{self.ga.optimum:.6f}\n"
        for i, var in enumerate(self.ga.optimum_variables):
            msg += f"    X{i+1}:\t{var:.6f}\n"
        msg += f"\nResults and plot have been successfully saved."
        QMessageBox.information(self, "Export complete", 
                            msg)