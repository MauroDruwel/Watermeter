import requests
import time
import logging
from datetime import datetime
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
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
        self.model = "gemini-2.5-flash"

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
            response = requests.get(config.ESP32_CAM_URL, timeout=15)
            response.raise_for_status()
            
            # Convert to PIL Image
            image = Image.open(BytesIO(response.content))
            logger.info("Image captured successfully")
            return image
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None

    def analyze_meter_with_gemini(self, image):
        """Send image to Gemini and extract water meter reading"""
        try:
            logger.info("Analyzing image with Gemini...")
            
            prompt = """
            Analyze this water meter image and extract the current reading.
            
            Please provide:
            1. The numeric reading shown on the meter (e.g., 123.456 or 123456)
            2. The unit if visible (m³, liters, etc.)
            3. Your confidence level (high/medium/low)
            
            Format your response as:
            Reading: [number]
            Unit: [unit]
            Confidence: [level]
            
            If you cannot read the meter clearly, explain why.
            """
            
            response = client.models.generate_content(
                model=self.model, contents=[
      prompt,
      types.Part.from_bytes(
        data=image,
        mime_type='image/jpeg',
      )
    ]
            )
            result = response.text
            
            logger.info(f"Gemini response: {result}")
            
            # Parse the reading from the response
            reading = self.parse_reading(result)
            return reading, result
            
        except Exception as e:
            logger.error(f"Error analyzing image with Gemini: {e}")
            return None, str(e)

    def parse_reading(self, gemini_response):
        """Extract numeric reading from Gemini response"""
        try:
            lines = gemini_response.split('\n')
            for line in lines:
                if 'Reading:' in line:
                    # Extract number from the line
                    parts = line.split('Reading:')[1].strip()
                    # Remove any non-numeric characters except decimal point
                    reading = ''.join(c for c in parts.split()[0] if c.isdigit() or c == '.')
                    return float(reading) if reading else None
        except Exception as e:
            logger.error(f"Error parsing reading: {e}")
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
                    'last_updated': datetime.now().isoformat(),
                    'gemini_response': raw_response[:500]  # Truncate if too long
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
            reading, raw_response = self.analyze_meter_with_gemini(image)
            
            if reading is None:
                logger.warning("Could not extract reading from image")
                logger.info(f"Raw Gemini response: {raw_response}")
                return
            
            # Step 5: Send to Home Assistant
            self.send_to_home_assistant(reading, raw_response)
            
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
