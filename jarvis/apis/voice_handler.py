"""
Voice Handler for Jarvis Bot
Handles text-to-speech and speech-to-text functionality
"""

import pyttsx3
import speech_recognition as sr
import threading
import time
from typing import Optional
import tempfile
import os
from gtts import gTTS
import pygame


class VoiceHandler:
    """
    Handles voice input and output for Jarvis Bot
    """
    
    def __init__(self, config):
        """
        Initialize voice handler
        
        Args:
            config: Configuration object
        """
        self.config = config
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ready to listen!")
        
        # Initialize pygame for audio playback (fallback)
        pygame.mixer.init()
        
        self.is_speaking = False
        self.temp_audio_dir = tempfile.mkdtemp()
    
    def _configure_tts(self):
        """Configure text-to-speech engine settings"""
        # Get available voices
        voices = self.tts_engine.getProperty('voices')
        
        # Set voice (prefer female voice if available)
        if voices:
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                # Use first available voice
                self.tts_engine.setProperty('voice', voices[0].id)
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', self.config.get('voice_rate', 200))
        self.tts_engine.setProperty('volume', self.config.get('voice_volume', 0.9))
    
    def speak(self, text: str, use_gtts: bool = False):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            use_gtts: Use Google TTS (requires internet) as fallback
        """
        if not text:
            return
        
        self.is_speaking = True
        
        try:
            if use_gtts:
                self._speak_with_gtts(text)
            else:
                # Use pyttsx3 for offline TTS
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
            # Fallback to Google TTS if pyttsx3 fails
            if not use_gtts:
                try:
                    self._speak_with_gtts(text)
                except Exception as fallback_error:
                    print(f"Fallback TTS also failed: {fallback_error}")
        
        self.is_speaking = False
    
    def _speak_with_gtts(self, text: str):
        """
        Use Google TTS for speech synthesis
        
        Args:
            text: Text to speak
        """
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            temp_file = os.path.join(self.temp_audio_dir, "temp_speech.mp3")
            tts.save(temp_file)
            
            # Play audio using pygame
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up temp file
            try:
                os.remove(temp_file)
            except:
                pass
                
        except Exception as e:
            raise Exception(f"Google TTS failed: {e}")
    
    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Timeout in seconds (None for no timeout)
        
        Returns:
            Recognized text or None if no speech detected
        """
        if self.is_speaking:
            return None
        
        try:
            timeout = timeout or self.config.get('timeout', 5)
            phrase_timeout = self.config.get('phrase_timeout', 2)
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )
            
            # Recognize speech using Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                # No speech detected or couldn't understand
                return None
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            # Timeout occurred, no speech detected
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def listen_continuously(self, callback_func, stop_event: threading.Event):
        """
        Listen continuously for voice input
        
        Args:
            callback_func: Function to call with recognized text
            stop_event: Threading event to stop listening
        """
        while not stop_event.is_set():
            try:
                text = self.listen(timeout=1)
                if text:
                    callback_func(text)
            except Exception as e:
                print(f"Error in continuous listening: {e}")
                time.sleep(1)
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Stop TTS engine
            if hasattr(self.tts_engine, 'stop'):
                self.tts_engine.stop()
            
            # Clean up temporary audio directory
            import shutil
            if os.path.exists(self.temp_audio_dir):
                shutil.rmtree(self.temp_audio_dir, ignore_errors=True)
            
            # Quit pygame
            pygame.mixer.quit()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def test_voice(self):
        """Test voice functionality"""
        print("Testing text-to-speech...")
        self.speak("Hello! I am Jarvis, your personal assistant. Voice test successful!")
        
        print("Testing speech recognition... Please say something:")
        text = self.listen(timeout=10)
        if text:
            print(f"I heard: {text}")
            self.speak(f"I heard you say: {text}")
        else:
            print("No speech detected")
            self.speak("I didn't hear anything. Please check your microphone.")