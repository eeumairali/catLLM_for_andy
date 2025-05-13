import sounddevice as sd
import wave
import speech_recognition as sr
import os

class AudioManager:
    def __init__(self):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
    
    def list_microphones(self):
        """List all available microphones and return them as a list"""
        devices = sd.query_devices()
        microphones = []
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:  # Only input devices
                microphones.append({
                    'index': i,
                    'name': device['name']
                })
        
        return microphones
    
    def record_audio(self, output_file, duration=5, sample_rate=48000, device_index=None):
        """Record audio from the specified microphone"""
        print(f"Recording from device {device_index} for {duration} seconds...")

        channels = 1  # Mono audio
        # Record audio
        audio_data = sd.rec(
            int(duration * sample_rate), 
            samplerate=sample_rate, 
            channels=channels, 
            dtype='int16', 
            device=device_index
        )
        sd.wait()  # Wait until recording is finished
        print("Recording finished!")

        # Save the audio to a WAV file
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
        
        print(f"Audio saved to {output_file}")
        return output_file
    
    def speech_to_text(self, wav_file_path):
        """Convert speech in a WAV file to text"""
        if not os.path.exists(wav_file_path):
            print(f"File {wav_file_path} not found.")
            return None

        # Process the audio file
        try:
            with sr.AudioFile(wav_file_path) as source:
                print("Converting audio to text...")
                audio_data = self.recognizer.record(source)
                
                # Perform speech recognition
                text = self.recognizer.recognize_google(audio_data)
                print(f"Speech recognition successful: '{text}'")
                return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An error occurred during speech-to-text conversion: {e}")
            return None