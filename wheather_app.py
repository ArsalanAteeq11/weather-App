# 

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: #f0f4f8;")
        self.setWindowIcon(QIcon("weather_icon.png"))  
        self.initUI()

    def initUI(self):
        # Fonts
        font_title = QFont("Arial", 20, QFont.Bold)
        font_label = QFont("Arial", 14)

        # Title Label
        self.title_label = QLabel("Weather Application")
        self.title_label.setFont(font_title)
        self.title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # City Input Section
        self.city_label = QLabel("Enter City Name:")
        self.city_label.setFont(font_label)
        self.city_label.setStyleSheet("color: #34495e;")

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("e.g., New York")
        self.city_input.setStyleSheet(
            "padding: 10px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px;"
        )

        # Search Button
        self.search_button = QPushButton("Get Weather")
        self.search_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.search_button.setStyleSheet(
            "background-color: #3498db; color: white; padding: 10px; border: none; border-radius: 5px;"
            "hover { background-color: #2980b9; }"
        )
        self.search_button.clicked.connect(self.get_weather)

        # Result Display Section
        self.result_label = QLabel("")
        self.result_label.setFont(font_label)
        self.result_label.setStyleSheet("color: #2c3e50; margin-top: 20px;")
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setWordWrap(True)

        # Layouts
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.city_label)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.result_label)
        main_layout.setAlignment(Qt.AlignTop)

        self.setLayout(main_layout)

    def get_weather(self):
        city_name = self.city_input.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        api_key = "092b355bc9775fd8dd5fa47c77124e7f"  # Replace with your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]

                self.result_label.setText(
                    f"<b>City:</b> {city_name}<br>"
                    f"<b>Weather:</b> {weather}<br>"
                    f"<b>Temperature:</b> {temp}°C<br>"
                    f"<b>Feels Like:</b> {feels_like}°C<br>"
                    f"<b>Humidity:</b> {humidity}%"
                )
            else:
                QMessageBox.warning(self, "API Error", "City not found or API error occurred.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
