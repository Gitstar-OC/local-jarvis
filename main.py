#!/usr/bin/env python3
"""
Local Jarvis - Personal AI Assistant
Main entry point for the Jarvis bot
"""

import click
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try importing dependencies, show helpful error if missing
try:
    from jarvis import JarvisBot
    from jarvis.utils.config import Config
    from jarvis.apis.voice_handler import VoiceHandler
    from jarvis.apis.calling_service import CallingService
    from jarvis.apis.weather_api import WeatherAPI
    from jarvis.apis.news_api import NewsAPI
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    IMPORT_ERROR = str(e)


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Local Jarvis - Your Personal AI Assistant"""
    pass


@cli.command()
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--voice-test', is_flag=True, help='Test voice functionality before starting')
def start(config, voice_test):
    """Start the Jarvis bot"""
    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ Dependencies not installed!")
        click.echo(f"Error: {IMPORT_ERROR}")
        click.echo("\nPlease install dependencies:")
        click.echo("pip install -r requirements.txt")
        sys.exit(1)
    
    click.echo("🤖 Starting Local Jarvis...")
    
    try:
        # Initialize bot
        bot = JarvisBot(config)
        
        # Test voice if requested
        if voice_test:
            click.echo("Testing voice functionality...")
            bot.voice_handler.test_voice()
            
            response = click.confirm("Voice test completed. Continue with startup?")
            if not response:
                click.echo("Startup cancelled.")
                return
        
        # Start the bot
        click.echo("Jarvis is starting up...")
        bot.start()
        
    except KeyboardInterrupt:
        click.echo("\n👋 Jarvis shutdown requested.")
    except Exception as e:
        click.echo(f"❌ Error starting Jarvis: {e}")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', help='Path to configuration file')
def test_voice(config):
    """Test voice functionality"""
    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ Dependencies not installed!")
        click.echo(f"Error: {IMPORT_ERROR}")
        click.echo("\nPlease install dependencies first:")
        click.echo("pip install -r requirements.txt")
        return
    
    click.echo("🎤 Testing voice functionality...")
    
    try:
        config_obj = Config(config)
        voice_handler = VoiceHandler(config_obj)
        voice_handler.test_voice()
        click.echo("✅ Voice test completed!")
        
    except Exception as e:
        click.echo(f"❌ Voice test failed: {e}")


@cli.command()
@click.option('--config', '-c', help='Path to configuration file')
def test_apis(config):
    """Test API connections"""
    if not DEPENDENCIES_AVAILABLE:
        click.echo("❌ Dependencies not installed!")
        click.echo(f"Error: {IMPORT_ERROR}")
        click.echo("\nPlease install dependencies first:")
        click.echo("pip install -r requirements.txt")
        return
    
    click.echo("🔗 Testing API connections...")
    
    try:
        config_obj = Config(config)
        
        # Test calling service
        click.echo("Testing Twilio calling service...")
        calling_service = CallingService(config_obj)
        if calling_service.test_connection():
            click.echo("✅ Twilio connection: OK")
        else:
            click.echo("❌ Twilio connection: Failed")
        
        # Test weather API
        click.echo("Testing weather API...")
        weather_api = WeatherAPI(config_obj)
        if weather_api.test_connection():
            click.echo("✅ Weather API connection: OK")
        else:
            click.echo("❌ Weather API connection: Failed")
        
        # Test news API
        click.echo("Testing news API...")
        news_api = NewsAPI(config_obj)
        if news_api.test_connection():
            click.echo("✅ News API connection: OK")
        else:
            click.echo("❌ News API connection: Failed")
        
        click.echo("🔗 API testing completed!")
        
    except Exception as e:
        click.echo(f"❌ API test failed: {e}")


@cli.command()
@click.option('--target', '-t', required=True, help='Phone number or contact name')
@click.option('--message', '-m', help='Message to speak during call')
@click.option('--config', '-c', help='Path to configuration file')
def call(target, message, config):
    """Make a phone call"""
    click.echo(f"📞 Making call to {target}...")
    
    try:
        config_obj = Config(config)
        calling_service = CallingService(config_obj)
        
        success = calling_service.make_call(target, message)
        if success:
            click.echo("✅ Call initiated successfully!")
        else:
            click.echo("❌ Failed to make call.")
            
    except Exception as e:
        click.echo(f"❌ Call failed: {e}")


@cli.command()
@click.option('--location', '-l', help='Location for weather')
@click.option('--config', '-c', help='Path to configuration file')
def weather(location, config):
    """Get weather information"""
    try:
        config_obj = Config(config)
        weather_api = WeatherAPI(config_obj)
        
        weather_info = weather_api.get_weather(location)
        if weather_info:
            click.echo(f"🌤️  {weather_info}")
        else:
            click.echo("❌ Could not get weather information.")
            
    except Exception as e:
        click.echo(f"❌ Weather request failed: {e}")


@cli.command()
@click.option('--category', '-c', help='News category')
@click.option('--config', help='Path to configuration file')
def news(category, config):
    """Get news headlines"""
    try:
        config_obj = Config(config)
        news_api = NewsAPI(config_obj)
        
        if category:
            headlines = news_api.get_category_news(category)
        else:
            headlines = news_api.get_headlines()
        
        if headlines:
            click.echo("📰 Latest Headlines:")
            for i, headline in enumerate(headlines, 1):
                click.echo(f"{i}. {headline}")
        else:
            click.echo("❌ Could not get news headlines.")
            
    except Exception as e:
        click.echo(f"❌ News request failed: {e}")


@cli.command()
def setup():
    """Setup Jarvis configuration"""
    click.echo("🔧 Setting up Local Jarvis...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        overwrite = click.confirm(".env file already exists. Overwrite?")
        if not overwrite:
            click.echo("Setup cancelled.")
            return
    
    # Copy .env.example to .env
    example_file = Path('.env.example')
    if example_file.exists():
        import shutil
        shutil.copy(example_file, env_file)
        click.echo("📋 Created .env file from template.")
    else:
        # Create basic .env file
        env_content = """# Local Jarvis Configuration
# Fill in your API keys below

# OpenAI API (optional, for advanced AI features)
OPENAI_API_KEY=

# Twilio (for calling functionality)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Weather API (OpenWeatherMap)
WEATHER_API_KEY=

# News API
NEWS_API_KEY=

# Voice settings
VOICE_RATE=200
VOICE_VOLUME=0.9

# Bot settings
BOT_NAME=Jarvis
USER_NAME=User
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        click.echo("📋 Created .env file.")
    
    click.echo("\n📝 Next steps:")
    click.echo("1. Edit the .env file and add your API keys")
    click.echo("2. Run 'python main.py test-apis' to verify your API connections")
    click.echo("3. Run 'python main.py test-voice' to test voice functionality")
    click.echo("4. Run 'python main.py start' to launch Jarvis")
    
    click.echo("\n🔑 API Keys needed:")
    click.echo("- Twilio: https://www.twilio.com/ (for calling)")
    click.echo("- OpenWeatherMap: https://openweathermap.org/api (for weather)")
    click.echo("- NewsAPI: https://newsapi.org/ (for news)")


if __name__ == '__main__':
    cli()