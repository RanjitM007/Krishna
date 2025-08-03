import speech_recognition as sr


def recognize_speech_from_mic():
    # Initialize recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        r.adjust_for_ambient_noise(source)  # Optional, reduces noise
        audio = r.listen(source)

    try:
        # Recognize speech using Google's free API
        text = r.recognize_google(audio, language='en-IN')  # 'en-IN' for Indian English
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

if __name__ == "__main__":
    recognize_speech_from_mic()
