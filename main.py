"""
Launches the 3D Weather desktop app with a GUI and OpenGL scene.
Initializes QApplication, shows the main window, and starts the event loop.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


os.environ["QT_OPENGL"] = "desktop"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
