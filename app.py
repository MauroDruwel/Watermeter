import requests
import time
import logging
from datetime import datetime
from google import genai
from google.genai import types
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Gemini
client = genai.Client()


class WaterMeterReader:
    def __init__(self):
        self.ha_headers = {
            'Authorization': f'Bearer {config.HOME_ASSISTANT_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.model = "gemini-2.5-flash-preview-09-2025"
        self.prompt = "Bekijk de foto van de watermeter heel zorgvuldig en vergroot waar nodig. De vier witte cijfers (wieltjes) geven het aantal kubieke meters (m³) — dat is het gehele getal vóór de komma. De vier rode wijzertjes geven de cijfers ná de komma (de decimale cijfers). Lees alle 8 cijfers exact en geef alleen de meterstand terug in één regel, zonder extra woorden of eenheid, in het format met een punt als decimaalscheiding: XXXX.YYYY (bijvoorbeeld 0123.4567). Als één of meer cijfers onleesbaar zijn of de foto onvoldoende kwaliteit heeft om de volledige acht cijfers betrouwbaar te bepalen, antwoord dan precies met: ERROR (uitroepende letters, met toelichting), tenzij het enkel over het laatste cijfer gaat, deze is minder belangrijk, dus probeer dan in te schatten wat het getal zou zijn."

    def is_within_active_hours(self):
        """Check if current time is within active hours"""
        now = datetime.now()
        current_hour = now.hour
        
        start_hour = config.ACTIVE_HOURS_START
        end_hour = config.ACTIVE_HOURS_END
        
        if start_hour <= end_hour:
            # Normal case: e.g., 6:00 to 23:00
            is_active = start_hour <= current_hour < end_hour
        else:
            # Overnight case: e.g., 22:00 to 6:00
            is_active = current_hour >= start_hour or current_hour < end_hour
        
        logger.info(f"Current hour: {current_hour:02d}:00, Active hours: {start_hour:02d}:00-{end_hour:02d}:00, Active: {is_active}")
        return is_active

    def configure_camera(self):
        """Configure camera settings before capture"""
        try:
            # Extract base URL from ESP32_CAM_URL (remove /capture endpoint)
            base_url = config.ESP32_CAM_URL.replace('/capture', '')
            
            # Camera settings to apply
            settings = [
                ('framesize', '15'),      # Set frame size (15 = UXGA 1600x1200)
                ('quality', '4'),         # Set JPEG quality (lower = better quality)
                ('hmirror', '1'),         # Horizontal mirror
                ('vflip', '1'),           # Vertical flip
                ('led_intensity', '35')   # LED intensity
            ]
            
            logger.info("Configuring camera settings...")
            for var, val in settings:
                url = f"{base_url}/control?var={var}&val={val}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                logger.info(f"Set {var}={val}")
                time.sleep(0.1)  # Small delay between settings
            
            # Wait a bit for settings to take effect
            time.sleep(0.5)
            logger.info("Camera configured successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error configuring camera: {e}")
            return False

    def capture_image(self):
        """Capture image from ESP32-CAM"""
        try:
            # Configure camera settings first
            if not self.configure_camera():
                logger.warning("Failed to configure camera, proceeding with capture anyway...")
            
            logger.info("Requesting image from ESP32-CAM...")
            image_bytes = requests.get(config.ESP32_CAM_URL).content
            image = types.Part.from_bytes(
            data=image_bytes, mime_type="image/jpeg"
            )
            return image
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None

    def analyze_meter_with_gemini(self, image):
        """Send image to Gemini and extract water meter reading"""
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=[self.prompt, image],
            )
            return float(response.text)
            
        except Exception as e:
            logger.error(f"Error analyzing image with Gemini: {e}")
            return None

    def send_to_home_assistant(self, reading):
        """Send the water meter reading to Home Assistant"""
        try:
            url = f'{config.HOME_ASSISTANT_URL}/api/services/input_number/set_value'
            
            data = {
                'entity_id': config.WATER_METER_INPUT,
                'value': reading
            }
            
            response = requests.post(url, json=data, headers=self.ha_headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Successfully sent reading {reading} to Home Assistant")
            return True
        except Exception as e:
            logger.error(f"Error sending data to Home Assistant: {e}")
            return False

    def read_meter(self):
        """Main function to read the water meter"""
        logger.info("=" * 50)
        logger.info(f"Starting water meter reading at {datetime.now()}")
        
        # Check if we're within active hours
        if not self.is_within_active_hours():
            logger.info("Outside of active hours, skipping reading")
            return
        
        try:
            # Step 1: Capture image
            image = self.capture_image()
            
            if image is None:
                logger.error("Failed to capture image")
                return
            
            # Step 2: Analyze with Gemini
            reading = self.analyze_meter_with_gemini(image)
            
            if reading is None:
                logger.warning("Could not extract reading from image")
                return
            
            # Step 3: Send to Home Assistant
            self.send_to_home_assistant(reading)

            logger.info(f"Water meter reading complete: {reading}")
            
        except Exception as e:
            logger.error(f"Error in read_meter: {e}")


def main():
    logger.info("Water Meter Reader starting...")
    logger.info(f"Reading interval: {config.READING_INTERVAL_MINUTES} minutes")
    
    # Validate configuration
    if not config.HOME_ASSISTANT_TOKEN:
        logger.error("HOME_ASSISTANT_TOKEN not set!")
        return
    
    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set!")
        return
    
    reader = WaterMeterReader()
    
    # Run once immediately on startup
    logger.info("Running initial reading...")
    reader.read_meter()
    
    # Keep running with simple sleep loop
    logger.info("Starting reading loop...")
    interval_seconds = config.READING_INTERVAL_MINUTES * 60
    
    while True:
        logger.info(f"Waiting {config.READING_INTERVAL_MINUTES} minutes until next reading...")
        time.sleep(interval_seconds)
        reader.read_meter()


if __name__ == '__main__':
    main()
