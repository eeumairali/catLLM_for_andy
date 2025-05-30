# AI Cat Assistant - Installation and Usage Guide

## Overview

The AI Cat Assistant is an application that combines:
- Voice recording and speech-to-text conversion
- Text processing using various LLM models (Gemma3, Llama3, Mistral, Phi3)
- Text-to-speech output
- Cat animations that change based on the active LLM model

## Installation

### Prerequisites
- Python 3.8 or newer
- tkinter (usually included with Python)
- pip (Python package manager)

### Required Libraries
Install the following dependencies:

```bash
pip install ollama pillow sounddevice wave SpeechRecognition gtts
```

### Optional
If you want to use actual LLM models locally:
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the models you want to use:
```bash
ollama pull gemma3
ollama pull llama3
ollama pull mistral
ollama pull phi3
```

## Project Structure
The application is divided into several Python files:

- `main.py`: Main application entry point
- `audio_manager.py`: Handles recording and speech-to-text conversion
- `text_processor.py`: Processes text using LLM models and handles text-to-speech
- `cat_animation.py`: Manages cat animations based on the selected model

## Directory Structure
```
/
├── main.py
├── audio_manager.py
├── text_processor.py
├── cat_animation.py
├── images/
│   ├── cat1.png  (for Gemma3)
│   ├── cat2.png  (for Llama3)
│   ├── cat3.png  (for Mistral)
│   └── cat4.png  (for Phi3)
```

## Usage

1. Run the application:
```bash
python main.py
```

2. The main window will open with:
   - A dropdown to select the LLM model
   - A cat image corresponding to the selected model
   - A text display area for the conversation
   - Input area for typing messages
   - Buttons for recording voice, sending text, and clearing chat

3. Using voice:
   - Click "Record Voice"
   - Select your microphone from the list
   - Speak for 5 seconds (the recording duration)
   - Your voice will be converted to text and processed

4. Using text:
   - Type your message in the text area
   - Click "Send Text"

5. The application will:
   - Display your message in the conversation area
   - Process your input using the selected LLM model
   - Show the response in the conversation area
   - Change the cat image based on the model
   - Speak the response aloud

6. You can switch between different LLM models using the dropdown menu.

## Troubleshooting

- If you don't have Ollama installed or the models pulled, the application will use mock responses.
- If you encounter issues with microphone recording, make sure your microphone is properly connected and selected.
- The application will create placeholder cat images if the actual images don't exist.

## Customization

You can customize the application by:
- Adding your own cat images to the `images` folder
- Modifying the mock responses in `text_processor.py`
- Adjusting the UI appearance in `main.py`
- Changing the recording duration in `audio_manager.py`