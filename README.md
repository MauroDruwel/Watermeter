

<p align="center">
	<img src="https://github.com/user-attachments/assets/c2290ed6-b191-4e1f-bdda-15a3271cc36f" alt="Home Assistant Screenshot" width="600" />
</p>

<h1 align="center">💧 Water Meter Reader</h1>
<p align="center"><b>"I just want to know my usage" Edition 🚀</b></p>

<p align="center">
	<a href="#-quick-install">Quickstart</a> |
	<a href="#%EF%B8%8F-getting-started">Getting Started</a> |
	<a href="#-project-structure">Project Structure</a> |
	<a href="#-contributing">Contributing</a>
</p>

---

> **Simple, modern, and AI-powered water meter reading for Home Assistant.**

---


## 📦 Quick Install

```sh
git clone https://github.com/MauroDruwel/Watermeter.git
cd Watermeter
copy .env.example .env  # On Windows, use 'copy', on Linux/Mac use 'cp'
# Fill in your .env with your API keys and config
docker-compose up -d
```

1. Flash your ESP32-CAM with the code in `CameraWebServer/` (see below)
2. Create a Home Assistant helper: `input_number.water_meter_reading`
3. Enjoy automatic water meter readings in Home Assistant! 💦

---

## Links

- [Documentation](#%EF%B8%8F-getting-started)
- [Contributing](#-contributing)
- [AI-on-the-edge-device (Inspiration)](https://github.com/jomjol/AI-on-the-edge-device)

---


## 🛠️ Getting Started

### 1. The Hardware (ESP32-CAM + Bling)

You'll need an ESP32-CAM and a WS2812B LED ring. Instead of the stock example, use the code in the `CameraWebServer` folder in this repo. It's got the special sauce for the LEDs. 🍝

1. Open `CameraWebServer/CameraWebServer.ino` in Arduino IDE.
2. Update your WiFi creds.
3. Flash it!
4. Hook up your LED ring (check the code for pins).

### 2. Home Assistant Setup

Create a helper so we have somewhere to put the numbers.
**Settings** → **Devices & Services** → **Helpers** → **Create Helper** → **Number**.
Call it `input_number.water_meter_reading`.

### 3. Docker (Because we love containers 🐳)

1. Copy the env file: `copy .env.example .env`
2. Fill in the blanks (API keys, URLs, etc.).
3. `docker-compose up -d`
4. Sit back and watch the magic happen.

---


## 📁 Project Structure

```
.
├── app.py                 # Main application logic
├── config.py              # Configuration management
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── test.py                # Testing script
├── CameraWebServer/       # Modified ESP32 code with WS2812B support
└── .env.example           # Environment variables template
```

---


## ⚙️ Configuration

Edit `.env` to set your options:

- `GEMINI_API_KEY`: Get this from Google (free tier available)
- `READING_INTERVAL_MINUTES`: How obsessed are you with your water usage?

---


## 🤖 How it Works

1. **Wakey Wakey**: The script runs every X minutes.
2. **Sanity Check**: It grabs the *previous* reading from Home Assistant. This helps us spot bad readings (because water meters don't run backwards... usually). 🕵️‍♂️
3. **Lights On**: It fires up the WS2812B LED ring (via the ESP32).
4. **Say Cheese 📸**: Snaps a pic of the meter.
5. **Lights Off**: Saves energy (and my eyes).
6. **AI Brain**: Sends the pic to Google Gemini to figure out the numbers.
7. **Home Assistant**: Dumps the data into HA so you can make pretty graphs. 📈

---


## 📖 The Story (or "Why did I do this?")

So, here's the tea ☕. I started this because I wanted to automate reading my water meter. My electricity meter is already digital and smart, but my water meter? Still stuck in the analog stone age (and probably will be for a while). 🦕

My first big brain idea 🧠 was to just turn on the garage lights to see the meter. I hooked it up to Home Assistant (because why not? 😎), but imagine having your garage lights flickering on and off in the middle of the night just to check how much water you used... yeah, spooky and not ideal. 👻

Next attempt: A simple LED. Result? A blinding beam of light and reflections everywhere. The camera couldn't see a thing! 🕶️

**The Solution:**
I ended up modifying the `CameraWebServer` source code to support a **WS2812B LED ring**. Now we get nice, even lighting without the disco ball effect. ✨
(Check out the `CameraWebServer` folder in this repo for the modified code!)

[Link to video coming soon!]

---

## 🧠 The AI Magic

I spent *way* too much time testing different Gemini models.
After battling with hallucinations and bad reads, I settled on **`gemini-2.5-flash-preview-09-2025`**.
Right now, it's the king 👑 of reading these analog dials, with it also being completely free. But hey, AI moves fast, so this might change next week.

I also tweaked the prompts until they were just right. It's not perfect, but it works like a charm for me!

---

## 🤝 Contributing

Got a better prompt? Found a cooler model? PRs are welcome! Let's make this thing even better. 🎉

---

*Made with ❤️, milk, and a lot of trial and error.*
