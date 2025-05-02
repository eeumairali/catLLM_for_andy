import ollama
from gtts import gTTS
import os

class ChatApp:
    def __init__(self, model_name='gemma3'):
        self.model_name = model_name
        self.messages = []

    def get_response(self, user_message):
        self.messages = [{'role': 'user', 'content': user_message}]
        response = ollama.chat(model=self.model_name, messages=self.messages)
        return response['message']['content']

    def speak(self, text, filename="response.mp3"):
        language = 'en'
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        os.system(f"open {filename}")

    def run(self):
        while True:
            user_input = input('Enter your message: ')
            if user_input.lower() in ['exit', 'quit']:
                print('Exiting the chat. Goodbye!')
                break
            response_text = self.get_response(user_input)
            print(f"Response: {response_text}")
            self.speak(response_text)

# To run the application
if __name__ == "__main__":
    app = ChatApp()
    app.run()