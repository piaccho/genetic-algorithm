def apply_styles(app):
  """Apply the cool blue theme to the entire application"""
  
  # Cool blue theme stylesheet
  app.setStyleSheet("""
      QMainWindow, QWidget {
          background-color: #1e2433;
          color: #e0e7ff;
      }
      
      QLabel {
          color: #e0e7ff;
          background-color: transparent;  /* Make label backgrounds transparent */
      }
      
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
      
      QPushButton {
          background-color: #3d5a80;
          color: white;
          border: 1px solid #5390d9;
          border-radius: 4px;
          padding: 5px 15px;
      }
      
      QPushButton:hover {
          background-color: #4a6fa5;
          border: 1px solid #48bfe3;
      }
      
      QPushButton:pressed {
          background-color: #2c4362;
      }
      
      QPushButton:disabled {
          background-color: #2c394b;
          color: #687693;
          border: 1px solid #415066;
      }
      
      QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
          background-color: #2c394b;
          color: #e0e7ff;
          border: 1px solid #3d5a80;
          border-radius: 4px;
          padding: 3px;
      }
      
      QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
          border: 1px solid #56cfe1;
      }
      
      QFrame {
          background-color: #263041;
          border-radius: 5px;
      }
      
      TimerWidget, VariablesWidget {
          background-color: #2c3e50;
          border: 1px solid #3d5a80;
          border-radius: 8px;
      }
      
      QCheckBox {
          color: #e0e7ff;
      }
      
      QCheckBox::indicator {
          width: 15px;
          height: 15px;
          background-color: #2c394b;
          border: 1px solid #3d5a80;
          border-radius: 3px;
      }
      
      QCheckBox::indicator:checked {
          background-color: #48bfe3;
      }
  """)