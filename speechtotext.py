import speech_recognition as sr
from gtts import gTTS
import os

def speech_to_text():
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
            
        print("Processing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return ""

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("afplay output.mp3")

print("Speech to Text Demo")
print("------------------")
text = speech_to_text()
if text:
    print("Converting your speech to audio...")
    text_to_speech(f"You said: {text}")