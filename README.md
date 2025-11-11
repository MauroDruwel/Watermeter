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
├── docker/                 # Python service running in Docker
│   ├── app.py             # Main application logic
│   ├── config.py          # Configuration management
│   ├── Dockerfile         # Docker image definition
│   ├── docker-compose.yml # Docker Compose configuration
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Docker setup instructions
│
└── esp32-cam/             # ESP32-CAM firmware
    ├── watermeter_cam.ino # Arduino sketch
    └── README.md          # ESP32-CAM setup instructions
```

## 🚀 How It Works

1. **Scheduled Reading**: Python service runs every X minutes (configurable)
2. **Light Control**: Turns on garage light via Home Assistant API
3. **Image Capture**: Requests image from ESP32-CAM
4. **Light Off**: Turns off the garage light
5. **AI Analysis**: Sends image to Google Gemini for meter reading extraction
6. **Data Storage**: Sends reading to Home Assistant as a sensor

## 🛠️ Quick Start

### 1. Set up ESP32-CAM

See detailed instructions in [`esp32-cam/README.md`](./esp32-cam/README.md)

- Flash the Arduino sketch to your ESP32-CAM
- Configure WiFi credentials
- Mount camera with clear view of water meter
- Note the IP address

### 2. Set up Docker Service

See detailed instructions in [`docker/README.md`](./docker/README.md)

1. Copy environment file:
   ```bash
   cd docker
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   - Home Assistant URL and token
   - ESP32-CAM IP address
   - Google Gemini API key
   - Reading interval

3. Start the service:
   ```bash
   docker-compose up -d
   ```

## 📋 Prerequisites

- **Hardware**:
  - ESP32-CAM module
  - USB-to-Serial adapter (for programming)
  - 5V power supply for ESP32-CAM
  - Smart light in Home Assistant (for illumination)

- **Software**:
  - Docker and Docker Compose
  - Home Assistant instance
  - Google Gemini API key (free tier available)
  - Arduino IDE (for ESP32-CAM setup)

## � API Keys & Tokens

### Home Assistant Long-Lived Access Token

1. Go to your Home Assistant profile
2. Scroll to "Long-Lived Access Tokens"
3. Create a token named "Water Meter Reader"
4. Copy and save in `.env`

### Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Copy and save in `.env`

## 📊 Home Assistant Integration

The service creates a sensor entity (default: `sensor.water_meter_reading`) that you can:
- Add to dashboards
- Use in automations
- Track historical usage
- Set up alerts

Example dashboard card:
```yaml
type: sensor
entity: sensor.water_meter_reading
name: Water Meter
icon: mdi:water
graph: line
```

## 🔧 Configuration

Key settings in `docker/.env`:

- `READING_INTERVAL_MINUTES`: How often to read (default: 60)
- `LIGHT_ON_DELAY`: Seconds to wait after light on (default: 2)
- `LIGHT_ENTITY_ID`: Your garage light entity ID
- `WATER_METER_SENSOR`: Sensor name in Home Assistant

## 📝 Logs

View logs from the Docker service:
```bash
cd docker
docker-compose logs -f
```

## 🐛 Troubleshooting

Common issues and solutions are documented in:
- [`docker/README.md`](./docker/README.md#troubleshooting)
- [`esp32-cam/README.md`](./esp32-cam/README.md#troubleshooting)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

See [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- ESP32-CAM community
- Google Gemini AI
- Home Assistant project
- Open source contributors

## � Support

If you encounter issues:
1. Check the README files in each folder
2. Review the logs
3. Open an issue on GitHub

---

**Made with ❤️ for smart home automation**
