from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, 
                            QCheckBox, QGroupBox, QFormLayout)

class ConfigForm(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create main horizontal layout to hold two columns
        main_layout = QHBoxLayout()
        
        # Create left column
        left_column = QVBoxLayout()
        
        # Function and bounds section
        bounds_group = QGroupBox("Problem Definition")
        bounds_layout = QFormLayout()
        
        self.fitness_function_combo = QComboBox(self)
        self.fitness_function_combo.addItems(['hyperellipsoid', 'rosenbrock'])
        bounds_layout.addRow(QLabel('Fitness Function:'), self.fitness_function_combo)
        
        self.lower_bound_input = QLineEdit(self)
        self.lower_bound_input.setText("-65.536")
        bounds_layout.addRow(QLabel('Lower Bound:'), self.lower_bound_input)
        
        self.upper_bound_input = QLineEdit(self)
        self.upper_bound_input.setText("65.536")
        bounds_layout.addRow(QLabel('Upper Bound:'), self.upper_bound_input)
        
        self.precision_input = QLineEdit(self)
        self.precision_input.setText("0.001")
        bounds_layout.addRow(QLabel('Precision:'), self.precision_input)
        
        self.num_variables_spin = QSpinBox(self)
        self.num_variables_spin.setRange(1, 100)
        self.num_variables_spin.setValue(2)
        bounds_layout.addRow(QLabel('Number of Variables:'), self.num_variables_spin)
        
        bounds_group.setLayout(bounds_layout)
        left_column.addWidget(bounds_group)
        
        # Population settings
        pop_group = QGroupBox("Population Settings")
        pop_layout = QFormLayout()
        
        self.population_size_spin = QSpinBox(self)
        self.population_size_spin.setRange(10, 1000)
        self.population_size_spin.setValue(50)
        pop_layout.addRow(QLabel('Population Size:'), self.population_size_spin)
        
        self.epochs_num_spin = QSpinBox(self)
        self.epochs_num_spin.setRange(1, 10000)
        self.epochs_num_spin.setValue(100)
        pop_layout.addRow(QLabel('Number of Epochs:'), self.epochs_num_spin)
        
        self.elite_amount_spin = QSpinBox(self)
        self.elite_amount_spin.setRange(0, 50)
        self.elite_amount_spin.setValue(2)
        pop_layout.addRow(QLabel('Elite Strategy Amount:'), self.elite_amount_spin)
        
        self.maximization_check = QCheckBox(self)
        pop_layout.addRow(QLabel('Maximization:'), self.maximization_check)
        
        pop_group.setLayout(pop_layout)
        left_column.addWidget(pop_group)
        
        # Create right column
        right_column = QVBoxLayout()
        
        # Genetic operations
        ops_group = QGroupBox("Genetic Operations")
        ops_layout = QFormLayout()
        
        self.crossover_prob_spin = QDoubleSpinBox(self)
        self.crossover_prob_spin.setRange(0.0, 1.0)
        self.crossover_prob_spin.setSingleStep(0.01)
        self.crossover_prob_spin.setValue(0.8)
        ops_layout.addRow(QLabel('Crossover Probability:'), self.crossover_prob_spin)
        
        self.mutation_prob_spin = QDoubleSpinBox(self)
        self.mutation_prob_spin.setRange(0.0, 1.0)
        self.mutation_prob_spin.setSingleStep(0.01)
        self.mutation_prob_spin.setValue(0.03)
        ops_layout.addRow(QLabel('Mutation Probability:'), self.mutation_prob_spin)
        
        self.inversion_prob_spin = QDoubleSpinBox(self)
        self.inversion_prob_spin.setRange(0.0, 1.0)
        self.inversion_prob_spin.setSingleStep(0.01)
        self.inversion_prob_spin.setValue(0.1)
        ops_layout.addRow(QLabel('Inversion Probability:'), self.inversion_prob_spin)
        
        ops_group.setLayout(ops_layout)
        right_column.addWidget(ops_group)
        
        # Selection methods
        selection_group = QGroupBox("Selection Method")
        selection_layout = QFormLayout()
        
        self.selection_method_combo = QComboBox(self)
        self.selection_method_combo.addItems(['tournament', 'roulette', 'best'])
        selection_layout.addRow(QLabel('Selection Method:'), self.selection_method_combo)
        
        self.select_best_amount_spin = QSpinBox(self)
        self.select_best_amount_spin.setRange(1, 100)
        self.select_best_amount_spin.setValue(10)
        selection_layout.addRow(QLabel('Best Selection Amount:'), self.select_best_amount_spin)
        
        self.tournament_size_spin = QSpinBox(self)
        self.tournament_size_spin.setRange(2, 50)
        self.tournament_size_spin.setValue(5)
        selection_layout.addRow(QLabel('Tournament Size:'), self.tournament_size_spin)
        
        selection_group.setLayout(selection_layout)
        right_column.addWidget(selection_group)
        
        # Crossover and mutation methods
        methods_group = QGroupBox("Genetic Methods")
        methods_layout = QFormLayout()
        
        self.crossover_method_combo = QComboBox(self)
        self.crossover_method_combo.addItems(['single_point', 'two_point', 'uniform', 'granular'])
        methods_layout.addRow(QLabel('Crossover Method:'), self.crossover_method_combo)
        
        self.mutation_method_combo = QComboBox(self)
        self.mutation_method_combo.addItems(['single_point', 'two_point', 'boundary'])
        methods_layout.addRow(QLabel('Mutation Method:'), self.mutation_method_combo)
        
        methods_group.setLayout(methods_layout)
        right_column.addWidget(methods_group)
        
        # Add columns to main layout
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column)
        
        # Create a container for the submit button to span both columns
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        
        # Submit button
        self.submit_button = QPushButton('Start Algorithm', self)
        self.submit_button.setMinimumHeight(40)  # Make button taller
        button_layout.addWidget(self.submit_button)
        
        # Create final layout to combine columns and button
        final_layout = QVBoxLayout()
        column_container = QWidget()
        column_container.setLayout(main_layout)
        final_layout.addWidget(column_container)
        final_layout.addWidget(button_container)
        
        self.setLayout(final_layout)


def get_config_params_from_gui(form):
    """
    Parse all form values and return a dictionary with configuration parameters
    """
    params = {}
    
    # Parse problem definition
    params['fitness_function'] = form.fitness_function_combo.currentText()
    params['lower_bound'] = float(form.lower_bound_input.text())
    params['upper_bound'] = float(form.upper_bound_input.text())
    params['precision'] = float(form.precision_input.text())
    params['num_variables'] = form.num_variables_spin.value()
    
    # Parse population settings
    params['population_size'] = form.population_size_spin.value()
    params['epochs_num'] = form.epochs_num_spin.value()
    params['elite_strategy_amount'] = form.elite_amount_spin.value()
    params['maximization'] = form.maximization_check.isChecked()
    
    # Parse genetic operations
    params['crossover_probability'] = form.crossover_prob_spin.value()
    params['mutation_probability'] = form.mutation_prob_spin.value()
    params['inversion_probability'] = form.inversion_prob_spin.value()
    
    # Parse selection method
    params['selection_method'] = form.selection_method_combo.currentText()
    params['select_best_amount'] = form.select_best_amount_spin.value()
    params['select_tournament_size'] = form.tournament_size_spin.value()
    
    # Parse genetic methods
    params['crossover_method'] = form.crossover_method_combo.currentText()
    params['mutation_method'] = form.mutation_method_combo.currentText()
    
    return params