"""
Core Jarvis Bot Implementation
Main bot class that orchestrates all functionalities
"""

import os
import sys
import time
import threading
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

# Voice and audio
import pyttsx3
import speech_recognition as sr

# Configuration
from dotenv import load_dotenv

# Utilities
from ..utils.logger import setup_logger
from ..utils.config import Config
from ..apis.voice_handler import VoiceHandler
from ..apis.calling_service import CallingService
from ..apis.weather_api import WeatherAPI
from ..apis.news_api import NewsAPI


class JarvisBot:
    """
    Main Jarvis Bot class that handles all core functionality
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Jarvis bot"""
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        self.logger = setup_logger()
        
        # Load configuration
        self.config = Config(config_path)
        
        # Initialize voice handler
        self.voice_handler = VoiceHandler(self.config)
        
        # Initialize services
        self.calling_service = CallingService(self.config)
        self.weather_api = WeatherAPI(self.config)
        self.news_api = NewsAPI(self.config)
        
        # Bot state
        self.is_listening = False
        self.is_running = False
        self.wake_word = self.config.get('wake_word', 'jarvis')
        
        # Command registry
        self.commands = self._register_commands()
        
        self.logger.info("Jarvis Bot initialized successfully")
    
    def _register_commands(self) -> Dict[str, callable]:
        """Register all available commands"""
        return {
            'call': self.make_call,
            'weather': self.get_weather,
            'news': self.get_news,
            'time': self.tell_time,
            'stop': self.stop_listening,
            'quit': self.shutdown,
            'help': self.show_help,
            'say': self.repeat_text,
        }
    
    def start(self):
        """Start the Jarvis bot"""
        self.logger.info("Starting Jarvis Bot...")
        self.is_running = True
        
        # Greet the user
        greeting = f"Hello! I'm {self.config.get('bot_name', 'Jarvis')}, your personal assistant. How can I help you today?"
        self.voice_handler.speak(greeting)
        
        try:
            self._main_loop()
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.shutdown()
    
    def _main_loop(self):
        """Main bot loop for listening and responding"""
        while self.is_running:
            try:
                # Listen for commands
                command = self.voice_handler.listen()
                
                if command:
                    self.logger.info(f"Received command: {command}")
                    self._process_command(command.lower())
                    
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(1)
    
    def _process_command(self, command: str):
        """Process a voice command"""
        # Check for wake word or direct commands
        if self.wake_word in command or self.is_listening:
            # Extract the actual command after wake word
            if self.wake_word in command:
                command = command.split(self.wake_word, 1)[-1].strip()
            
            # Find matching command
            for cmd_name, cmd_func in self.commands.items():
                if cmd_name in command:
                    try:
                        cmd_func(command)
                        return
                    except Exception as e:
                        self.logger.error(f"Error executing command {cmd_name}: {e}")
                        self.voice_handler.speak(f"Sorry, I encountered an error while executing that command.")
                        return
            
            # If no specific command found, try general conversation
            self._handle_general_query(command)
    
    def _handle_general_query(self, query: str):
        """Handle general queries that don't match specific commands"""
        response = f"I heard you say: {query}. I'm still learning how to respond to that."
        self.voice_handler.speak(response)
    
    # Command implementations
    def make_call(self, command: str):
        """Make a phone call"""
        # Extract phone number or contact name from command
        if "call" in command:
            target = command.split("call", 1)[-1].strip()
            if target:
                self.voice_handler.speak(f"Calling {target}")
                success = self.calling_service.make_call(target)
                if success:
                    self.voice_handler.speak("Call initiated successfully")
                else:
                    self.voice_handler.speak("Sorry, I couldn't make the call")
            else:
                self.voice_handler.speak("Who would you like me to call?")
    
    def get_weather(self, command: str):
        """Get weather information"""
        # Extract location from command if provided
        location = None
        if "weather" in command:
            parts = command.split("weather")
            if len(parts) > 1 and parts[1].strip():
                location = parts[1].strip().replace("in ", "").replace("for ", "")
        
        weather_info = self.weather_api.get_weather(location)
        if weather_info:
            self.voice_handler.speak(weather_info)
        else:
            self.voice_handler.speak("Sorry, I couldn't get weather information right now.")
    
    def get_news(self, command: str):
        """Get news headlines"""
        news = self.news_api.get_headlines()
        if news:
            self.voice_handler.speak("Here are the latest news headlines:")
            for headline in news[:3]:  # Limit to top 3 headlines
                self.voice_handler.speak(headline)
        else:
            self.voice_handler.speak("Sorry, I couldn't get news information right now.")
    
    def tell_time(self, command: str):
        """Tell current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.voice_handler.speak(f"The current time is {current_time}")
    
    def repeat_text(self, command: str):
        """Repeat text after 'say' command"""
        if "say" in command:
            text = command.split("say", 1)[-1].strip()
            if text:
                self.voice_handler.speak(text)
            else:
                self.voice_handler.speak("What would you like me to say?")
    
    def show_help(self, command: str):
        """Show available commands"""
        help_text = """
        Here are the commands I can help you with:
        - Call someone: 'Call John' or 'Call 555-1234'
        - Get weather: 'What's the weather?' or 'Weather in New York'
        - Get news: 'What's the news?' or 'Latest news'
        - Tell time: 'What time is it?'
        - Repeat text: 'Say hello world'
        - Stop listening: 'Stop'
        - Quit: 'Quit' or 'Exit'
        """
        self.voice_handler.speak(help_text)
    
    def stop_listening(self, command: str):
        """Stop listening for commands"""
        self.is_listening = False
        self.voice_handler.speak("I'll stop listening now. Say my wake word to activate me again.")
    
    def shutdown(self, command: str = None):
        """Shutdown the bot"""
        self.logger.info("Shutting down Jarvis Bot...")
        self.is_running = False
        self.voice_handler.speak("Goodbye! Have a great day!")
        
        # Cleanup resources
        if hasattr(self.voice_handler, 'cleanup'):
            self.voice_handler.cleanup()
        
        sys.exit(0)