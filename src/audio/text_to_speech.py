#!/usr/bin/env python3
"""
TextToSpeech class for multi-language text-to-speech conversion
Part of the audio module
"""

import os
import sys
import tempfile
import threading
import time
from gtts import gTTS
import pygame
from typing import Optional, Dict, List, Union

class TextToSpeech:
    """Multi-language Text-to-Speech class using Google TTS"""
    
    def __init__(self):
        """Initialize the TextToSpeech class"""
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese (Mandarin)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'bn': 'Bengali',
            'ur': 'Urdu',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'cs': 'Czech',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'sk': 'Slovak',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sr': 'Serbian',
            'uk': 'Ukrainian',
            'el': 'Greek',
            'he': 'Hebrew',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Filipino',
            'sw': 'Swahili',
            'af': 'Afrikaans',
            'ta': 'Tamil',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'mr': 'Marathi',
            'or': 'Odia',
            'as': 'Assamese',
            'ne': 'Nepali'
        }
        
        # Hinglish patterns and detection
        self.hinglish_keywords = [
            'hai', 'hain', 'kar', 'kya', 'kaise', 'kahan', 'kab', 'kyun', 'kaun',
            'aur', 'main', 'hum', 'tum', 'aap', 'yeh', 'woh', 'iske', 'uske',
            'mera', 'tera', 'hamara', 'tumhara', 'apka', 'iska', 'uska',
            'karna', 'hona', 'jana', 'aana', 'lena', 'dena', 'dekha', 'suna',
            'accha', 'bura', 'bada', 'chota', 'naya', 'purana', 'thik', 'galat',
            'bahut', 'kam', 'zyada', 'sab', 'kuch', 'koi', 'sabko', 'kisiko'
        ]
        
        self.current_language = 'en'
        self.slow_speech = False
        self._audio_initialized = False
        self._init_audio()
    
    def _init_audio(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init()
            self._audio_initialized = True
        except Exception as e:
            print(f"Warning: Could not initialize audio: {e}")
            self._audio_initialized = False
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and names"""
        return self.supported_languages.copy()
    
    def list_languages(self) -> None:
        """Print all supported languages"""
        print("\n=== Supported Languages ===")
        print("Code\tLanguage")
        print("-" * 25)
        for code, name in sorted(self.supported_languages.items()):
            print(f"{code}\t{name}")
        print()
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the default language for TTS
        
        Args:
            language_code (str): Language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            bool: True if language is supported, False otherwise
        """
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def set_speed(self, slow: bool = False) -> None:
        """
        Set speech speed
        
        Args:
            slow (bool): True for slow speech, False for normal speed
        """
        self.slow_speech = slow
    
    def speak(self, text: str, language: Optional[str] = None, slow: Optional[bool] = None,voice_id: Optional[str] = None) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to convert to speech
            language (str, optional): Language code. Uses current_language if None
            slow (bool, optional): Speech speed. Uses slow_speech setting if None
            
        Returns:
            bool: True if successful, False otherwise
        """
        lang = language or self.current_language
        speed = slow if slow is not None else self.slow_speech
        
        return self._generate_and_play(text, lang, speed)
    
    def save(self, text: str, filename: str, language: Optional[str] = None, slow: Optional[bool] = None) -> bool:
        """
        Convert text to speech and save to file
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename
            language (str, optional): Language code. Uses current_language if None
            slow (bool, optional): Speech speed. Uses slow_speech setting if None
            
        Returns:
            bool: True if successful, False otherwise
        """
        lang = language or self.current_language
        speed = slow if slow is not None else self.slow_speech
        
        return self._generate_audio(text, lang, speed, filename)
    
    def speak_and_save(self, text: str, filename: str, language: Optional[str] = None, slow: Optional[bool] = None) -> bool:
        """
        Convert text to speech, save to file, and play it
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename
            language (str, optional): Language code. Uses current_language if None
            slow (bool, optional): Speech speed. Uses slow_speech setting if None
            
        Returns:
            bool: True if successful, False otherwise
        """
        lang = language or self.current_language
        speed = slow if slow is not None else self.slow_speech
        
        if self._generate_audio(text, lang, speed, filename):
            if self._audio_initialized:
                self._play_audio_file(filename)
            return True
        return False
    
    def _generate_and_play(self, text: str, language: str, slow: bool ,voice_id: Optional[str] = None) -> bool:
        """Generate TTS audio and play it directly"""
        try:
            if language not in self.supported_languages:
                print(f"Error: Language '{language}' not supported.")
                return False
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Create temporary file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tmp_filename = tmp_file.name
            tmp_file.close()  # Close the file so gTTS can write to it
            
            try:
                # Save audio to temporary file
                tts.save(tmp_filename)
                
                if self._audio_initialized:
                    self._play_audio_file(tmp_filename)
                else:
                    print("Audio playback not available. Audio saved temporarily.")
                
            finally:
                # Clean up temporary file
                try:
                    if os.path.exists(tmp_filename):
                        os.unlink(tmp_filename)
                except Exception as cleanup_error:
                    print(f"Warning: Could not delete temporary file: {cleanup_error}")
            
            return True
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return False
    
    def _generate_audio(self, text: str, language: str, slow: bool, filename: str) -> bool:
        """Generate TTS audio and save to file"""
        try:
            if language not in self.supported_languages:
                print(f"Error: Language '{language}' not supported.")
                return False
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(filename)
            
            return True
            
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def _play_audio_file(self, filename: str) -> None:
        """Play audio file using pygame"""
        if not self._audio_initialized:
            print("Audio playback not available.")
            return
            
        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"Audio file not found: {filename}")
                return
            
            # Load and play the audio file
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
            # Try alternative method using pygame.mixer.Sound
            try:
                sound = pygame.mixer.Sound(filename)
                sound.play()
                # Wait for sound to finish
                while pygame.mixer.get_busy():
                    time.sleep(0.1)
            except Exception as e2:
                print(f"Alternative playback also failed: {e2}")
    
    def stop(self) -> None:
        """Stop current audio playback"""
        if self._audio_initialized:
            pygame.mixer.music.stop()
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        if self._audio_initialized:
            return pygame.mixer.music.get_busy()
        return False
    
    def detect_hinglish(self, text: str) -> bool:
        """
        Detect if text contains Hinglish (Hindi-English mix)
        
        Args:
            text (str): Text to analyze
            
        Returns:
            bool: True if Hinglish is detected
        """
        text_lower = text.lower()
        hinglish_count = 0
        english_count = 0
        
        words = text_lower.split()
        
        for word in words:
            if word in self.hinglish_keywords:
                hinglish_count += 1
        
        # If more than 20% of words are common Hinglish words, consider it Hinglish
        if len(words) > 0 and (hinglish_count / len(words)) > 0.2:
            return True
            
        return False
    
    def auto_detect_language(self, text: str) -> str:
        """
        Auto-detect language from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Detected language code
        """
        # Check for Devanagari script (Hindi)
        devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        if devanagari_count > len(text) * 0.3:
            return 'hi'
        
        # Check for Hinglish
        if self.detect_hinglish(text):
            return 'hi'  # Use Hindi TTS for Hinglish
            
        # Default to current language
        return self.current_language
    
    def speak_hinglish(self, text: str, slow: bool = False, auto_detect: bool = True) -> bool:
        """
        Speak Hinglish text with optimal settings
        
        Args:
            text (str): Hinglish text to speak
            slow (bool): Speech speed
            auto_detect (bool): Whether to auto-detect language
            
        Returns:
            bool: True if successful
        """
        if auto_detect:
            lang = self.auto_detect_language(text)
        else:
            lang = 'hi'  # Force Hindi
            
        return self.speak(text, language=lang, slow=slow)
    
    def speak_hindi(self, text: str, slow: bool = False, voice_id: Optional[str] = None) -> bool:
        """Speak text in Hindi"""
        return self.speak(text, 'hi', slow,voice_id=voice_id)
    
    def speak_tamil(self, text: str, slow: bool = False) -> bool:
        """Speak text in Tamil"""  
        return self.speak(text, 'ta', slow)
    
    def speak_telugu(self, text: str, slow: bool = False) -> bool:
        """Speak text in Telugu"""
        return self.speak(text, 'te', slow)
    
    def speak_gujarati(self, text: str, slow: bool = False) -> bool:
        """Speak text in Gujarati"""
        return self.speak(text, 'gu', slow)
    
    def speak_punjabi(self, text: str, slow: bool = False) -> bool:
        """Speak text in Punjabi"""
        return self.speak(text, 'pa', slow)
    
    def speak_marathi(self, text: str, slow: bool = False) -> bool:
        """Speak text in Marathi"""
        return self.speak(text, 'mr', slow)
    
    # Convenience methods for different languages
    def speak_english(self, text: str, slow: bool = False) -> bool:
        """Speak text in English"""
        return self.speak(text, 'en', slow)
    
    def speak_spanish(self, text: str, slow: bool = False) -> bool:
        """Speak text in Spanish"""
        return self.speak(text, 'es', slow)
    
    def speak_french(self, text: str, slow: bool = False) -> bool:
        """Speak text in French"""
        return self.speak(text, 'fr', slow)
    
    def speak_german(self, text: str, slow: bool = False) -> bool:
        """Speak text in German"""
        return self.speak(text, 'de', slow)
    
    def speak_japanese(self, text: str, slow: bool = False) -> bool:
        """Speak text in Japanese"""
        return self.speak(text, 'ja', slow)
    
    def speak_chinese(self, text: str, slow: bool = False) -> bool:
        """Speak text in Chinese"""
        return self.speak(text, 'zh', slow)
    
    def __call__(self, text: str, language: Optional[str] = None, slow: Optional[bool] = None) -> bool:
        """
        Make the class callable - same as speak() method
        
        Args:
            text (str): Text to convert to speech
            language (str, optional): Language code
            slow (bool, optional): Speech speed
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.speak(text, language, slow)
    
    def __repr__(self) -> str:
        """String representation of the TTS object"""
        return f"TextToSpeech(language='{self.current_language}', slow={self.slow_speech})"

