import os
from dotenv import load_dotenv

load_dotenv()

# Home Assistant Configuration
HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL', 'http://localhost:8123')
HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN')
SWITCH_ENTITY_ID = os.getenv('SWITCH_ENTITY_ID', 'switch.garage_lamp')

# ESP32-CAM Configuration
ESP32_CAM_URL = os.getenv('ESP32_CAM_URL', 'http://esp32-cam.local/capture')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Home Assistant Sensor for Water Meter
WATER_METER_SENSOR = os.getenv('WATER_METER_SENSOR', 'sensor.water_meter_reading')

# Schedule Configuration (in minutes)
READING_INTERVAL_MINUTES = int(os.getenv('READING_INTERVAL_MINUTES', '60'))

# Switch timing (in seconds)
SWITCH_ON_DELAY = int(os.getenv('SWITCH_ON_DELAY', '2'))
