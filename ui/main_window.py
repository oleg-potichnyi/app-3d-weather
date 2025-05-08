"""
This module contains the implementation of the main application window,
which includes an OpenGL widget, a weather panel, and control buttons.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QTimer
from gl.cube_widget import CubeWidget
from services.weather_service import get_weather


class MainWindow(QMainWindow):
    """Main application window: contains a 3D widget, controls, and weather information."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Weather App")
        self.setFixedSize(800, 600)
        self._initialize_ui()
        self._initialize_timer()
        self._update_weather()

    def _initialize_ui(self) -> None:
        """Set up the user interface layout and widgets."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.cube_widget = CubeWidget()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter the name of the city")
        self.city_input.setText("Kyiv")

        self.refresh_button = QPushButton("Update weather")
        self.refresh_button.clicked.connect(self._update_weather)

        self.reset_button = QPushButton("Reset position")
        self.reset_button.clicked.connect(self.cube_widget.reset_view)

        self.weather_label = QLabel("Temperature: -- °C")
        self.description_label = QLabel("State: --")

        weather_layout = QVBoxLayout()
        weather_layout.addWidget(self.city_input)
        weather_layout.addWidget(self.refresh_button)
        weather_layout.addWidget(self.weather_label)
        weather_layout.addWidget(self.description_label)
        weather_layout.addStretch()
        weather_layout.addWidget(self.reset_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.cube_widget, stretch=3)
        main_layout.addLayout(weather_layout, stretch=1)
        central_widget.setLayout(main_layout)

    def _initialize_timer(self) -> None:
        """Initialize and start a timer for periodic weather updates."""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_weather)
        self.timer.start(600000)

    def _update_weather(self) -> None:
        """Fetch and display the current weather for the entered city."""
        city = self.city_input.text()
        if not city:
            QMessageBox.warning(self, "Warning", "Please enter the name of the city.")
            return
        try:
            data = get_weather(city)
            temp = data["current_condition"][0]["temp_C"]
            desc = data["current_condition"][0]["weatherDesc"][0]["value"]

            self.weather_label.setText(f"Temperature: {temp} °C")
            self.description_label.setText(f"State: {desc}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not get weather: {e}")
