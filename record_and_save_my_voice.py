# pip install sounddevice
import sounddevice as sd
import wave

def list_microphones():
    print("Available Microphones:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:  # Only list input devices
            print(f"{i}: {device['name']}")

def record_audio(output_file, duration, sample_rate=48000, device_index=None):
    print("Recording...")
    # Record audio using the specified microphone
    audio_data = sd.rec(
        int(duration * sample_rate), 
        samplerate=sample_rate, 
        channels=1, 
        dtype='int16', 
        device=device_index
    )
    sd.wait()  # Wait until recording is finished
    print("Recording finished!")

    # Save the audio to a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    print(f"Audio saved to {output_file}")

# Example usage
if __name__ == "__main__":
    # List available microphones
    list_microphones()

    # Ask the user to select a microphone
    try:
        device_index = int(input("Enter the index of the microphone you want to use: "))
    except ValueError:
        print("Invalid input. Using the default microphone.")
        device_index = None

    # Record audio
    output_file = "computer.wav"  # Output file name
    duration = 10  # Duration in seconds
    record_audio(output_file, duration, device_index=device_index)