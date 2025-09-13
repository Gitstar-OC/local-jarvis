"""
Weather API integration for Jarvis Bot
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime


class WeatherAPI:
    """
    Weather information service using OpenWeatherMap API
    """
    
    def __init__(self, config):
        """
        Initialize weather API
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.api_key = config.get('weather_api_key')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.default_location = config.get('default_location', 'New York')
        
        if not self.api_key:
            print("Weather API key not configured. Weather functionality disabled.")
    
    def get_weather(self, location: Optional[str] = None) -> Optional[str]:
        """
        Get current weather for a location
        
        Args:
            location: Location name (optional, uses default if not provided)
        
        Returns:
            Weather description string or None if failed
        """
        if not self.api_key:
            return "Weather service is not configured. Please add your OpenWeatherMap API key."
        
        location = location or self.default_location
        
        try:
            # Get weather data
            weather_data = self._fetch_weather_data(location)
            if not weather_data:
                return None
            
            # Format weather information
            return self._format_weather_response(weather_data, location)
            
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None
    
    def get_forecast(self, location: Optional[str] = None, days: int = 3) -> Optional[str]:
        """
        Get weather forecast for a location
        
        Args:
            location: Location name
            days: Number of days for forecast (1-5)
        
        Returns:
            Forecast description string or None if failed
        """
        if not self.api_key:
            return "Weather service is not configured."
        
        location = location or self.default_location
        
        try:
            # Get forecast data
            forecast_data = self._fetch_forecast_data(location)
            if not forecast_data:
                return None
            
            # Format forecast information
            return self._format_forecast_response(forecast_data, location, days)
            
        except Exception as e:
            print(f"Error getting forecast: {e}")
            return None
    
    def _fetch_weather_data(self, location: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch current weather data from API
        
        Args:
            location: Location name
        
        Returns:
            Weather data dictionary or None if failed
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'imperial'  # Fahrenheit
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Weather API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def _fetch_forecast_data(self, location: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch weather forecast data from API
        
        Args:
            location: Location name
        
        Returns:
            Forecast data dictionary or None if failed
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Forecast API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
            return None
    
    def _format_weather_response(self, data: Dict[Any, Any], location: str) -> str:
        """
        Format weather data into a readable response
        
        Args:
            data: Weather data from API
            location: Location name
        
        Returns:
            Formatted weather description
        """
        try:
            # Extract weather information
            main = data['main']
            weather = data['weather'][0]
            wind = data.get('wind', {})
            
            temperature = round(main['temp'])
            feels_like = round(main['feels_like'])
            humidity = main['humidity']
            description = weather['description'].title()
            
            # Build response
            response = f"The current weather in {location} is {description}. "
            response += f"Temperature is {temperature} degrees Fahrenheit, "
            response += f"feels like {feels_like} degrees. "
            response += f"Humidity is {humidity} percent."
            
            # Add wind information if available
            if 'speed' in wind:
                wind_speed = round(wind['speed'])
                response += f" Wind speed is {wind_speed} miles per hour."
            
            return response
            
        except KeyError as e:
            print(f"Missing expected weather data: {e}")
            return f"I got some weather data for {location}, but it seems incomplete."
        except Exception as e:
            print(f"Error formatting weather response: {e}")
            return f"I found weather information for {location}, but couldn't format it properly."
    
    def _format_forecast_response(self, data: Dict[Any, Any], location: str, days: int) -> str:
        """
        Format forecast data into a readable response
        
        Args:
            data: Forecast data from API
            location: Location name
            days: Number of days for forecast
        
        Returns:
            Formatted forecast description
        """
        try:
            forecasts = data['list']
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in forecasts:
                date = datetime.fromtimestamp(item['dt']).date()
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Build response
            response = f"Here's the weather forecast for {location}: "
            
            count = 0
            for date, day_forecasts in list(daily_forecasts.items())[:days]:
                if count >= days:
                    break
                
                # Get midday forecast for the day
                midday_forecast = day_forecasts[len(day_forecasts)//2]
                
                temp = round(midday_forecast['main']['temp'])
                description = midday_forecast['weather'][0]['description'].title()
                
                day_name = date.strftime('%A') if count == 0 else date.strftime('%A, %B %d')
                response += f"{day_name}: {description}, {temp} degrees. "
                
                count += 1
            
            return response
            
        except Exception as e:
            print(f"Error formatting forecast response: {e}")
            return f"I found forecast information for {location}, but couldn't format it properly."
    
    def test_connection(self) -> bool:
        """
        Test weather API connection
        
        Returns:
            True if connection is working, False otherwise
        """
        if not self.api_key:
            return False
        
        try:
            test_data = self._fetch_weather_data("London")
            return test_data is not None
        except Exception:
            return False