"""
Launches the 3D Weather desktop app with a GUI and OpenGL scene.

Initializes QApplication, shows the main window, and starts the event loop.
"""
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
