"""
Local Jarvis - Your Personal AI Assistant
A bot that can call and talk on your behalf with multiple additional features.
"""

__version__ = "1.0.0"
__author__ = "Local Jarvis Team"

# Optional import to handle missing dependencies gracefully
try:
    from .core.bot import JarvisBot
    __all__ = ['JarvisBot']
except ImportError as e:
    print(f"Warning: Some dependencies missing. Please install requirements: {e}")
    __all__ = []