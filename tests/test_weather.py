import unittest
from unittest.mock import patch
from services.weather_service import get_weather
from PyQt5.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow
import re


class TestWeatherService(unittest.TestCase):
    """Testing the get_weather function."""

    @patch("services.weather_service.requests.get")
    def test_get_weather_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [
                {"temp_C": "25", "weatherDesc": [{"value": "clear sky"}]}
            ]
        }

        result = get_weather("Kyiv")
        self.assertIn("Kyiv", result)
        self.assertIn("25", result)
        self.assertIn("clear sky", result)

    @patch("services.weather_service.requests.get")
    def test_get_weather_city_not_found(self, mock_get):
        mock_get.return_value.status_code = 404
        result = get_weather("UnknownCity")
        self.assertEqual(result, "Error: 404")


class TestWeatherIcons(unittest.TestCase):
    """Testing weather icon URLs."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()

    def test_clear_description(self):
        url = self.window._get_weather_icon_url("clear sky")
        self.assertIn("01d", url)

    def test_rain_description(self):
        url = self.window._get_weather_icon_url("light rain")
        self.assertIn("09d", url)

    def test_unknown_description(self):
        url = self.window._get_weather_icon_url("foggy weather")
        self.assertIn("50d", url)


def parse_weather_string(data: str):
    """Helper function for parsing (logic moved out of main_window.py)."""
    match = re.match(r"([A-Za-z\s]+):\s*(\d+)(°C),\s*(.+)", data)
    if not match:
        raise ValueError("Unable to parse weather data")
    return {
        "city": match.group(1),
        "temp": int(match.group(2)),
        "unit": match.group(3),
        "desc": match.group(4),
    }


class TestWeatherParsing(unittest.TestCase):
    """Testing the parsing function."""

    def test_parse_weather_string_valid(self):
        data = "Kyiv: 25°C, clear sky"
        result = parse_weather_string(data)
        self.assertEqual(result["city"], "Kyiv")
        self.assertEqual(result["temp"], 25)
        self.assertEqual(result["unit"], "°C")
        self.assertEqual(result["desc"], "clear sky")

    def test_parse_weather_string_invalid(self):
        data = "Invalid string"
        with self.assertRaises(ValueError):
            parse_weather_string(data)
