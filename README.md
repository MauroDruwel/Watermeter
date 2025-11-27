# 💧 Water Meter Reader - The "I just want to know my usage" Edition 🚀

Welcome to my water meter reading project! This isn't just another AI wrapper, it's a journey of trial, error, and blinking LEDs. 😅

## � Inspiration & Why I Built This

There's already an amazing project out there called [AI-on-the-edge-device](https://github.com/jomjol/AI-on-the-edge-device). It's super powerful, but it felt a bit heavy for what I needed. It requires specific hardware and a lot of manual setup (like selecting the specific dials on the image).

I thought, *"With today's modern AI, surely we can just throw a picture at an LLM and have it figure it out, right?"* 🤔
So, I decided to build my own version—simpler, less configuration, and powered by the latest AI models.

##  The Story (or "Why did I do this?")

So, here's the tea ☕. I started this because I wanted to automate reading my water meter. My electricity meter is already digital and smart, but my water meter? Still stuck in the analog stone age (and probably will be for a while). 🦕

My first big brain idea 🧠 was to just turn on the garage lights to see the meter. I hooked it up to Home Assistant (because why not? 😎), but imagine having your garage lights flickering on and off in the middle of the night just to check how much water you used... yeah, spooky and not ideal. 👻

Next attempt: A simple LED. Result? A blinding beam of light and reflections everywhere. The camera couldn't see a thing! 🕶️

**The Solution:**
I ended up modifying the `CameraWebServer` source code to support a **WS2812B LED ring**. Now we get nice, even lighting without the disco ball effect. ✨
(Check out the `CameraWebServer` folder in this repo for the modified code!)

[Link to video coming soon!]

## 🤖 The AI Magic

I spent *way* too much time testing different Gemini models.
After battling with hallucinations and bad reads, I settled on **`gemini-2.5-flash-preview-09-2025`**.
Right now, it's the king 👑 of reading these analog dials, with it also being completely free. But hey, AI moves fast, so this might change next week.

I also tweaked the prompts until they were just right. It's not perfect, but it works like a charm for me!

## 🛠️ How it actually works

1.  **Wakey Wakey**: The script runs every X minutes.
2.  **Sanity Check**: It grabs the *previous* reading from Home Assistant. This helps us spot bad readings (because water meters don't run backwards... usually). 🕵️‍♂️
3.  **Lights On**: It fires up the WS2812B LED ring (via the ESP32).
4.  **Say Cheese 📸**: Snaps a pic of the meter.
5.  **Lights Off**: Saves energy (and my eyes).
6.  **AI Brain**: Sends the pic to Google Gemini to figure out the numbers.
7.  **Home Assistant**: Dumps the data into HA so I can make pretty graphs. 📈

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

## 🚀 Getting Started (The Boring but Necessary Stuff)

### 1. The Hardware (ESP32-CAM + Bling)

You'll need an ESP32-CAM and a WS2812B LED ring.
Instead of the stock example, use the code in the `CameraWebServer` folder in this repo. It's got the special sauce for the LEDs. 🍝

1.  Open `CameraWebServer/CameraWebServer.ino` in Arduino IDE.
2.  Update your WiFi creds.
3.  Flash it!
4.  Hook up your LED ring (check the code for pins).

### 2. Home Assistant Setup

Create a helper so we have somewhere to put the numbers.
**Settings** → **Devices & Services** → **Helpers** → **Create Helper** → **Number**.
Call it `input_number.water_meter_reading`.

### 3. Docker (Because we love containers 🐳)

1.  Copy the env file: `cp .env.example .env`
2.  Fill in the blanks (API keys, URLs, etc.).
3.  `docker-compose up -d`
4.  Sit back and watch the magic happen.

## � Config Stuff

Check `.env` for the knobs and dials you can turn.
*   `GEMINI_API_KEY`: Get this from Google. It's free (mostly).
*   `READING_INTERVAL_MINUTES`: How obsessed are you with your water usage?

## 🤝 Contributing

Got a better prompt? Found a cooler model? PRs are welcome! Let's make this thing even better.

---
*Made with ❤️, milk, and a lot of trial and error.*
