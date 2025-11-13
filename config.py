import os
from dotenv import load_dotenv

load_dotenv()

# Home Assistant Configuration
HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL', 'http://localhost:8123')
HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN')

# ESP32-CAM Configuration
ESP32_CAM_URL = os.getenv('ESP32_CAM_URL', 'http://esp32-cam.local/capture')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Home Assistant Input Number for Water Meter
WATER_METER_INPUT = os.getenv('WATER_METER_INPUT', 'input_number.water_meter_reading')

# Schedule Configuration (in minutes)
READING_INTERVAL_MINUTES = int(os.getenv('READING_INTERVAL_MINUTES', '60'))

# Active Hours Configuration (24-hour format)
# Readings will only be taken between these hours
ACTIVE_HOURS_START = int(os.getenv('ACTIVE_HOURS_START', '6'))   # Default: 6:00 AM
ACTIVE_HOURS_END = int(os.getenv('ACTIVE_HOURS_END', '23'))      # Default: 11:00 PM

# Safety Configuration
# Maximum allowed difference between readings (in cubic meters)
# This prevents accepting readings that are unrealistically high
MAX_READING_DIFFERENCE = float(os.getenv('MAX_READING_DIFFERENCE', '1000'))
