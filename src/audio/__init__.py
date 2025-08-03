"""
Audio processing module
Contains text-to-speech functionality and related audio utilities
"""

from .text_to_speech import TextToSpeech

__version__ = "1.0.0"
__author__ = "Ranjit M"
__all__ = ['TextToSpeech']

# Make TextToSpeech directly available from audio module
__all__ = ['TextToSpeech']