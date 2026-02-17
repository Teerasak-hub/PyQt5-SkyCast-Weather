import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Weather Forecast", self)
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name...")
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("SkyCast | Python Weather")
        self.setFixedSize(450, 650)

        # ใช้ Layout หลัก
        vbox = QVBoxLayout()
        vbox.setContentsMargins(30, 40, 30, 40)
        vbox.setSpacing(15)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)

        # เพิ่มเส้นคั่นนิดนึงให้ดูเป็นสัดส่วน
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: rgba(255, 255, 255, 50);")
        vbox.addWidget(line)

        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        for widget in [self.city_label, self.city_input, self.temperature_label,
                       self.emoji_label, self.description_label]:
            widget.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
            }
            QLabel {
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#city_label {
                font-size: 32px;
                font-weight: bold;
                color: #4cc9f0; /* สีฟ้าสว่าง */
                margin-bottom: 10px;
            }
            QLineEdit#city_input {
                font-size: 20px;
                padding: 12px;
                border: 2px solid #4cc9f0;
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 10);
                color: white;
            }
            QPushButton#get_weather_button {
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                background-color: #4cc9f0;
                color: #1a1a2e;
                border-radius: 12px;
                margin-top: 5px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #4361ee;
                color: white;
            }
            QLabel#temperature_label {
                font-size: 80px;
                font-weight: bold;
                margin-top: 20px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                margin: 10px;
            }
            QLabel#description_label {
                font-size: 28px;
                text-transform: capitalize;
                color: #b0b0b0;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            error_msg = f"Error {response.status_code}:"
            match response.status_code:
                case 404:
                    self.display_error(f"{error_msg}\nCity not found")
                case 401:
                    self.display_error(f"{error_msg}\nInvalid API Key")
                case _:
                    self.display_error(f"HTTP Error occurred")
        except Exception as e:
            self.display_error("Check Connection")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 25px; color: #ff4d4d;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 80px; color: white;")

        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temp_c:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        return "❓"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())