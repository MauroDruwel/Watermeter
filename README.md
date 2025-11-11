# Water Meter Reader

Automated water meter reading system using ESP32-CAM, Google Gemini AI, and Home Assistant integration.

## 🎯 Overview

This project automatically reads your analog water meter using:
- **ESP32-CAM** for capturing images of the meter
- **Google Gemini AI** for intelligent meter reading extraction
- **Home Assistant** for light control and data storage
- **Docker** for easy deployment

## 📁 Project Structure

```
.
├── app.py                 # Main application logic
├── config.py              # Configuration management
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── test.py                # Testing script
└── .env.example           # Environment variables template
```

## 🚀 How It Works

1. **Scheduled Reading**: Python service runs every X minutes (configurable)
2. **Light Control**: Turns on garage light via Home Assistant API
3. **Image Capture**: Requests image from ESP32-CAM
4. **Light Off**: Turns off the garage light
5. **AI Analysis**: Sends image to Google Gemini for meter reading extraction
6. **Data Storage**: Updates `input_number.water_meter_reading` in Home Assistant

## 🛠️ Quick Start

### 1. Set up ESP32-CAM

**Flash the CameraWebServer Example**

1. Install Arduino IDE and ESP32 board support
2. Use the official ESP32 CameraWebServer example:
   - GitHub: [ESP32 CameraWebServer](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer)
   - In Arduino IDE: `File` → `Examples` → `ESP32` → `Camera` → `CameraWebServer`

3. Configure the sketch:
   - Set your WiFi credentials (`ssid` and `password`)
   - Select your ESP32-CAM board model
   - Upload to your ESP32-CAM

4. After upload:
   - Open Serial Monitor (115200 baud)
   - Note the IP address displayed
   - Test by visiting `http://<ESP32-IP>/capture` in your browser

5. Mount the camera with a clear view of your water meter

### 2. Set up Home Assistant

Create an input number helper for storing the water meter reading:

1. Go to **Settings** → **Devices & Services** → **Helpers**
2. Click **Create Helper** → **Number**
3. Configure:
   - **Name**: Water Meter Reading
   - **Entity ID**: `input_number.water_meter_reading`
   - **Minimum**: 0
   - **Maximum**: 10000

### 3. Set up Docker Service

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   - `HOME_ASSISTANT_URL`: Your Home Assistant URL
   - `HOME_ASSISTANT_TOKEN`: Long-lived access token
   - `ESP32_CAM_URL`: Your ESP32-CAM capture URL (e.g., `http://192.168.1.127/capture`)
   - `SWITCH_ENTITY_ID`: Entity ID of your light/switch for illumination
   - `WATER_METER_INPUT`: `input_number.water_meter_reading`
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `READING_INTERVAL_MINUTES`: How often to read (default: 60)

3. Start the service:
   ```bash
   docker-compose up -d
   ```

4. Check logs:
   ```bash
   docker-compose logs -f
   ```

## 📋 Prerequisites

- **Hardware**:
  - ESP32-CAM module
  - 5V power supply for ESP32-CAM
  - Smart light or switch in Home Assistant (for illumination)

- **Software**:
  - Docker and Docker Compose
  - Home Assistant instance with API access
  - Google Gemini API key (free tier available at [Google AI Studio](https://makersuite.google.com/app/apikey))
  - Arduino IDE with ESP32 board support (for ESP32-CAM setup)

## 🔑 API Keys & Tokens

### Home Assistant Long-Lived Access Token

1. Go to your Home Assistant profile
2. Scroll to "Long-Lived Access Tokens"
3. Create a token named "Water Meter Reader"
4. Copy and save in `.env`

### Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Copy and save in `.env`

## 🔧 Configuration

Key settings in `.env`:

- `HOME_ASSISTANT_URL`: Your Home Assistant URL (e.g., `http://192.168.1.148:8123`)
- `HOME_ASSISTANT_TOKEN`: Long-lived access token from Home Assistant
- `SWITCH_ENTITY_ID`: Entity ID of light/switch for illumination (e.g., `switch.garage_lamp`)
- `ESP32_CAM_URL`: ESP32-CAM capture endpoint (e.g., `http://192.168.1.127/capture`)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `WATER_METER_INPUT`: Input number entity ID (default: `input_number.water_meter_reading`)
- `READING_INTERVAL_MINUTES`: How often to read the meter (default: 60)
- `SWITCH_ON_DELAY`: Seconds to wait after turning on light (default: 2)

## 📝 Logs

View logs from the Docker service:
```bash
docker-compose logs -f
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

See [LICENSE](./LICENSE) file for details.



**Made with ❤️ for smart home automation**
