import sys
from PyQt5.QtWidgets import QApplication
from views import MainWindow
from styles import apply_styles

def main():
    app = QApplication(sys.argv)
    apply_styles(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()