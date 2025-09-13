"""
Configuration management for Jarvis Bot
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """
    Configuration manager for Jarvis Bot
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config_data = {}
        self._load_defaults()
        
        if config_path and Path(config_path).exists():
            self._load_from_file(config_path)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_defaults(self):
        """Load default configuration values"""
        self.config_data = {
            'bot_name': 'Jarvis',
            'user_name': 'User',
            'wake_word': 'jarvis',
            'voice_rate': 200,
            'voice_volume': 0.9,
            'language': 'en-US',
            'timeout': 5,
            'phrase_timeout': 2,
            'default_location': 'New York',
        }
    
    def _load_from_file(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                self.config_data.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'OPENAI_API_KEY': 'openai_api_key',
            'TWILIO_ACCOUNT_SID': 'twilio_account_sid',
            'TWILIO_AUTH_TOKEN': 'twilio_auth_token',
            'TWILIO_PHONE_NUMBER': 'twilio_phone_number',
            'WEATHER_API_KEY': 'weather_api_key',
            'NEWS_API_KEY': 'news_api_key',
            'BOT_NAME': 'bot_name',
            'USER_NAME': 'user_name',
            'VOICE_RATE': 'voice_rate',
            'VOICE_VOLUME': 'voice_volume',
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert numeric values
                if config_key in ['voice_rate']:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                elif config_key in ['voice_volume']:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                
                self.config_data[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value
    
    def save(self, config_path: str):
        """
        Save configuration to file
        
        Args:
            config_path: Path to save configuration file
        """
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config to {config_path}: {e}")
    
    def __str__(self) -> str:
        """String representation of configuration"""
        # Don't expose sensitive information
        safe_config = {k: v for k, v in self.config_data.items() 
                      if 'key' not in k.lower() and 'token' not in k.lower() and 'sid' not in k.lower()}
        return json.dumps(safe_config, indent=2)