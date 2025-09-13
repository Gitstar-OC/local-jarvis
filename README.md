# Local Jarvis - Personal AI Assistant

A Python-based personal assistant bot that can call and talk on your behalf with multiple additional features.

## Features

🗣️ **Voice Communication**
- Text-to-speech synthesis
- Speech recognition
- Voice commands
- Wake word activation

📞 **Calling Functionality**
- Make phone calls using Twilio
- Voice message delivery
- Contact management
- Call history

🌤️ **Weather Information**
- Current weather conditions
- Weather forecasts
- Multiple location support

📰 **News Updates**
- Latest headlines
- Category-specific news
- News search functionality

🤖 **Personal Assistant**
- Time and date information
- Voice-controlled interactions
- Customizable responses
- Extensible plugin system

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Gitstar-OC/local-jarvis.git
   cd local-jarvis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup configuration:**
   ```bash
   python main.py setup
   ```

4. **Add API keys to `.env` file:**
   - Twilio credentials (for calling)
   - OpenWeatherMap API key (for weather)
   - NewsAPI key (for news)

## Quick Start

### 1. Test your setup
```bash
# Test voice functionality
python main.py test-voice

# Test API connections
python main.py test-apis
```

### 2. Start Jarvis
```bash
python main.py start
```

### 3. Voice Commands
Once running, you can use these voice commands:

- **"Jarvis, what's the weather?"** - Get current weather
- **"Jarvis, call John"** - Make a phone call
- **"Jarvis, what's the news?"** - Get latest headlines
- **"Jarvis, what time is it?"** - Get current time
- **"Jarvis, say hello world"** - Text-to-speech test
- **"Jarvis, help"** - List available commands
- **"Jarvis, stop"** - Stop listening
- **"Jarvis, quit"** - Shutdown

## CLI Commands

### Start the bot
```bash
python main.py start [--config CONFIG_FILE] [--voice-test]
```

### Make a call
```bash
python main.py call -t "555-1234" [-m "Your message"]
```

### Get weather
```bash
python main.py weather [-l "New York"]
```

### Get news
```bash
python main.py news [-c technology]
```

### Test functionality
```bash
python main.py test-voice
python main.py test-apis
```

## Configuration

### Environment Variables (.env file)
```env
# Twilio (for calling functionality)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number

# Weather API (OpenWeatherMap)
WEATHER_API_KEY=your_weather_api_key

# News API
NEWS_API_KEY=your_news_api_key

# Voice settings
VOICE_RATE=200
VOICE_VOLUME=0.9

# Bot settings
BOT_NAME=Jarvis
USER_NAME=User
```

### Getting API Keys

1. **Twilio** (for calling): https://www.twilio.com/
   - Create account and get Account SID, Auth Token, and phone number

2. **OpenWeatherMap** (for weather): https://openweathermap.org/api
   - Free tier available with 1000 calls/day

3. **NewsAPI** (for news): https://newsapi.org/
   - Free tier available with 1000 requests/day

## Project Structure

```
local-jarvis/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── jarvis/                # Main package
│   ├── __init__.py
│   ├── core/              # Core bot functionality
│   │   ├── __init__.py
│   │   └── bot.py         # Main bot class
│   ├── apis/              # API integrations
│   │   ├── __init__.py
│   │   ├── voice_handler.py
│   │   ├── calling_service.py
│   │   ├── weather_api.py
│   │   └── news_api.py
│   ├── utils/             # Utilities
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── plugins/           # Future plugins
│       └── __init__.py
```

## Usage Examples

### Voice Interaction
1. Say "Jarvis" to wake the bot
2. Give your command: "What's the weather in London?"
3. Jarvis will respond with voice and text

### Phone Calls
```python
# Through voice command
"Jarvis, call mom"

# Through CLI
python main.py call -t "+1234567890" -m "This is a test call from Jarvis"
```

### Weather Queries
```python
# Through voice command
"Jarvis, what's the weather?"
"Jarvis, weather in Tokyo"

# Through CLI
python main.py weather -l "Tokyo"
```

## Troubleshooting

### Audio Issues
- **No audio output**: Check speaker connections and volume
- **No microphone input**: Check microphone permissions and connections
- **Poor recognition**: Ensure quiet environment and clear speech

### API Issues
- **Calling fails**: Verify Twilio credentials and phone number format
- **Weather fails**: Check OpenWeatherMap API key and location name
- **News fails**: Verify NewsAPI key and internet connection

### Dependencies
- **PyAudio installation**: May require system-level audio libraries
  - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
  - macOS: `brew install portaudio`
  - Windows: Usually works with pip install

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Built with ❤️ using Python, Twilio, OpenWeatherMap, and NewsAPI** 
