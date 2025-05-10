"""
This module contains the implementation of the main application window,
which includes an OpenGL widget, a weather panel, and control buttons.
"""
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from gl.cube_widget import CubeWidget
from services.weather_service import get_weather
import re


class MainWindow(QMainWindow):
    """Main application window: contains a 3D widget,
    controls, and weather information."""

    def __init__(self) -> None:
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
        self.city_label = QLabel("City: --")

        self.icon_label = QLabel()

        weather_layout = QVBoxLayout()
        weather_layout.addWidget(self.city_input)
        weather_layout.addWidget(self.refresh_button)
        weather_layout.addWidget(self.city_label)
        weather_layout.addWidget(self.weather_label)
        weather_layout.addWidget(self.description_label)
        weather_layout.addWidget(self.icon_label)

        self.color_buttons = []
        for i in range(6):
            button = QPushButton(f"Change color for face {i + 1}")
            button.clicked.connect(lambda _, i=i: self.change_face_color(i))
            self.color_buttons.append(button)
            weather_layout.addWidget(button)

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
            QMessageBox.warning(
                self, "Warning", "Please enter the name of the city."
            )
            return
        try:
            data = get_weather(city)
            if not data:
                QMessageBox.warning(
                    self,
                    "City not found",
                    f"Could not find weather for {city}"
                )
                return
            if isinstance(data, str):
                match = re.match(r"([A-Za-z\s]+):\s*(\d+)(°C),\s*(.+)", data)
                if match:
                    city_name = match.group(1)
                    temp = match.group(2)
                    unit = match.group(3)
                    desc = match.group(4)
                    print(f"Weather description: '{desc}'")

                    self.city_label.setText(f"City: {city_name}")
                    self.weather_label.setText(f"Temperature: {temp} {unit}")
                    self.description_label.setText(f"State: {desc}")
                    icon_url = self._get_weather_icon_url(desc)
                    pixmap = self._load_pixmap_from_url(icon_url)
                    self.icon_label.setPixmap(pixmap)
                else:
                    raise ValueError("Unable to parse weather data")
            else:
                raise ValueError("Weather data is not in the expected format")
        except ValueError as ve:
            QMessageBox.critical(
                self, "Invalid data", f"Error in data format: {ve}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not get weather: {e}")

    def _load_pixmap_from_url(self, url: str) -> QPixmap:
        """
        Loads a weather icon image from the given URL
        and returns it as a scaled QPixmap.
        """
        try:
            import requests

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            image = QImage()
            image.loadFromData(response.content)
            return QPixmap.fromImage(image).scaled(64, 64)
        except Exception as e:
            print(f"Error loading icon: {e}")
            return QPixmap()

    def _get_weather_icon_url(self, description: str) -> str:
        """
        Returns the appropriate weather icon URL based
        on the weather description text.
        """
        desc = description.lower()
        print(f"Normalized description: '{desc}'")

        if "clear" in desc or "sun" in desc:
            return "https://openweathermap.org/img/wn/01d@2x.png"
        elif "cloud" in desc:
            return "https://openweathermap.org/img/wn/04d@2x.png"
        elif "rain" in desc:
            return "https://openweathermap.org/img/wn/09d@2x.png"
        elif "snow" in desc:
            return "https://openweathermap.org/img/wn/13d@2x.png"
        else:
            return "https://openweathermap.org/img/wn/50d@2x.png"

    def change_face_color(self, index: int) -> None:
        """
        Opens a color picker dialog
        and changes the color of the specified cube face.
        """
        self.cube_widget.choose_color(index)
