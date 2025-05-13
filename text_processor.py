import ollama
from gtts import gTTS
import os
import tkinter as tk
import time

class TextProcessor:
    def __init__(self):
        # Keep track of conversation history for each model
        self.model_conversations = {
            "gemma3": [],
            "llama3": [],
            "mistral": [],
            "phi3": []
        }
        
        # Mock responses for models that might not be installed
        self.mock_responses = {
            "gemma3": "I'm Gemma, a helpful and friendly AI assistant. How can I help you today?",
            "llama3": "Hello! I'm Llama, ready to assist with your questions and tasks.",
            "mistral": "Greetings! I'm Mistral, here to provide insights and assistance.",
            "phi3": "Hi there! I'm Phi, your helpful AI companion. What can I do for you?"
        }
    
    def get_response(self, user_message, model_name="gemma3"):
        """Get a response from the LLM model"""
        # Add the user message to conversation history
        if model_name not in self.model_conversations:
            self.model_conversations[model_name] = []
        
        # Add the new message
        self.model_conversations[model_name].append({
            'role': 'user', 
            'content': user_message
        })
        
        # Try to get response from Ollama
        try:
            # Create a copy of the conversation history to send to the model
            messages = self.model_conversations[model_name].copy()
            
            # Get response from Ollama
            response = ollama.chat(
                model=model_name, 
                messages=messages
            )
            
            # Extract the response text
            response_text = response['message']['content']
            
            # Add the assistant's response to the conversation history
            self.model_conversations[model_name].append({
                'role': 'assistant',
                'content': response_text
            })
            
            return response_text
        
        except Exception as e:
            print(f"Error getting response from {model_name}: {e}")
            
            # Provide a mock response if Ollama fails
            mock_response = f"I'm having trouble connecting to the {model_name} model. "
            mock_response += self.mock_responses.get(model_name, "How can I help you?")
            
            # Add the mock response to the conversation history
            self.model_conversations[model_name].append({
                'role': 'assistant',
                'content': mock_response
            })
            
            return mock_response
    
    def speak(self, text, filename="response.mp3"):
        """Convert text to speech and play it"""
        try:
            # Create a temporary file if the path doesn't exist
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Convert text to speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            
            # Play the audio file
            if os.name == 'posix':  # macOS or Linux
                os.system(f"open {filename}")
            elif os.name == 'nt':  # Windows
                os.system(f"start {filename}")
            else:
                print(f"Audio saved to {filename}, but couldn't automatically play it.")
        
        except Exception as e:
            print(f"Error in text-to-speech: {e}")