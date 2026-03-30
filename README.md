# 🌦️ Real-Time Weather and AQI Tracker

## 📌 Overview
Real-Time Weather and AQI Tracker is a command-line Python application that fetches and displays live weather data and Air Quality Index (AQI) information for a user-provided city using Open-Meteo APIs.

---

## 🚀 Features
- Convert city name to latitude and longitude
- Fetch real-time weather data
- Display Air Quality Index (AQI)
- Shows PM2.5 and PM10 values
- Retry mechanism for stable API calls
- Simple command-line interface

---

## 🛠️ Requirements
- Python 3.x
- requests library

---

## 📦 Installation
Install dependencies:

    pip install requests

---

## ▶️ Usage
Run the script:

    python weather_aqi_tracker.py

Enter the city name when prompted.

---

## ⚙️ How It Works
1. Converts city name into coordinates  
2. Fetches weather and AQI data from APIs  
3. Handles API failures using retry logic  
4. Displays formatted results in terminal  

---

## 🧠 Core Functions

| Function | Description |
|---------|------------|
| fetch_with_retry | Handles API requests with retry logic |
| get_coordinates | Converts city name to latitude & longitude |
| fetch_weather_and_aqi_data | Fetches weather and AQI data |
| display_results | Displays output in console |

---

## 📁 Project Structure

    .
    ├── weather_aqi_tracker.py
    ├── README.md
    └── project_statement.md

---

## 🔮 Future Improvements
- Add GUI interface  
- Support multiple cities  
- Add weather forecast  
- Export data to file  

---

## 🤝 Contributing
Feel free to fork this repository and submit pull requests.

---

## 📜 License
This project is open-source and available under the MIT License.
