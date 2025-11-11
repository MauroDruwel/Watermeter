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
        self.prompt = "Bekijk de foto van de watermeter heel zorgvuldig en vergroot waar nodig. De vier witte cijfers (wieltjes) geven het aantal kubieke meters (m³) — dat is het gehele getal vóór de komma. De vier rode wijzertjes geven de cijfers ná de komma (de decimale cijfers). Lees alle 8 cijfers exact en geef alleen de meterstand terug in één regel, zonder extra woorden of eenheid, in het format met een punt als decimaalscheiding: XXXX.YYYY (bijvoorbeeld 0123.4567). Als één of meer cijfers onleesbaar zijn of de foto onvoldoende kwaliteit heeft om de volledige acht cijfers betrouwbaar te bepalen, antwoord dan precies met: ERROR (uitroepende letters, zonder toelichting)."

    def control_switch(self, state: bool):
        """Turn the garage switch on or off"""
        try:
            service = 'turn_on' if state else 'turn_off'
            url = f'{config.HOME_ASSISTANT_URL}/api/services/switch/{service}'
            data = {'entity_id': config.SWITCH_ENTITY_ID}
            
            response = requests.post(url, json=data, headers=self.ha_headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Switch {'turned on' if state else 'turned off'} successfully")
            return True
        except Exception as e:
            logger.error(f"Error controlling switch: {e}")
            return False

    def capture_image(self):
        """Capture image from ESP32-CAM"""
        try:
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

    def send_to_home_assistant(self, reading, raw_response):
        """Send the water meter reading to Home Assistant"""
        try:
            url = f'{config.HOME_ASSISTANT_URL}/api/states/{config.WATER_METER_SENSOR}'
            
            data = {
                'state': reading,
                'attributes': {
                    'unit_of_measurement': 'm³',
                    'friendly_name': 'Water Meter Reading',
                    'last_updated': datetime.now().isoformat()
                }
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
        
        try:
            # Step 1: Turn on the switch
            if not self.control_switch(True):
                logger.error("Failed to turn on switch, aborting")
                return
            
            # Wait for light to stabilize
            time.sleep(config.SWITCH_ON_DELAY)
            
            # Step 2: Capture image
            image = self.capture_image()
            
            # Step 3: Turn off the switch
            self.control_switch(False)
            
            if image is None:
                logger.error("Failed to capture image")
                return
            
            # Step 4: Analyze with Gemini
            reading = self.analyze_meter_with_gemini(image)
            
            if reading is None:
                logger.warning("Could not extract reading from image")
                return
            
            # Step 5: Send to Home Assistant
            self.send_to_home_assistant(reading)

            logger.info(f"Water meter reading complete: {reading}")
            
        except Exception as e:
            logger.error(f"Error in read_meter: {e}")
            # Make sure switch is turned off even if there's an error
            try:
                self.control_switch(False)
            except:
                pass


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
