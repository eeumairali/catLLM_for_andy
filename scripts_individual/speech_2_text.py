import speech_recognition as sr
import os

def wav_to_text(wav_file_path):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the WAV file
    with sr.AudioFile(wav_file_path) as source:
        print("Converting audio to text...")
        audio_data = recognizer.record(source)

    # Perform speech recognition
    try:
        text = recognizer.recognize_google(audio_data)
        print("Conversion successful!")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Example usage
if __name__ == "__main__":
    wav_file = "computer.wav"  # Replace with your WAV file path
    if os.path.exists(wav_file):
        result = wav_to_text(wav_file)
        if result:
            print("Transcribed Text:")
            print(result)
    else:
        print(f"File {wav_file} not found.")