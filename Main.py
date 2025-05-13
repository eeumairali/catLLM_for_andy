import tkinter as tk
from audio_manager import AudioManager
from text_processor import TextProcessor
from cat_animation import CatAnimation
import threading
import os

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cat Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Current LLM model - initialize before other components
        self.current_model = "gemma3"  # Default model
        self.available_models = ["llama3", "gemma3", "mistral", "phi3"]
        
        # Initialize components       self.audio_manager = AudioManager()
        self.text_processor = TextProcessor()
        self.cat_animation = CatAnimation(self.root)
        
        # Create UI
        self.setup_ui()

    def setup_ui(self):
        # Create frames
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        middle_frame = tk.Frame(self.root, bg="#f0f0f0")
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Top frame - Model selection
        model_label = tk.Label(top_frame, text="Select LLM Model:", bg="#f0f0f0", font=("Arial", 12))
        model_label.pack(side=tk.LEFT, padx=5)
        
        self.model_var = tk.StringVar(value=self.current_model)
        model_dropdown = tk.OptionMenu(top_frame, self.model_var, *self.available_models, command=self.change_model)
        model_dropdown.config(width=10, font=("Arial", 12))
        model_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Middle frame - Cat animation and conversation
        self.cat_animation.setup_in_frame(middle_frame)
        
        # Text display area
        text_frame = tk.Frame(middle_frame, bg="#f0f0f0")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.conversation_text = tk.Text(text_frame, height=10, width=60, font=("Arial", 12))
        self.conversation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.conversation_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conversation_text.config(yscrollcommand=scrollbar.set)
        self.conversation_text.config(state=tk.DISABLED)
        
        # Bottom frame - Input and controls
        text_input_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
        text_input_frame.pack(fill=tk.X, pady=5)
        
        self.input_text = tk.Text(text_input_frame, height=3, width=50, font=("Arial", 12))
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        button_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=5)
        
        # Buttons
        self.record_button = tk.Button(button_frame, text="Record Voice", command=self.record_audio, 
                                     width=15, font=("Arial", 12), bg="#4CAF50", fg="blue")
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.send_button = tk.Button(button_frame, text="Send Text", command=self.process_text_input, 
                                    width=15, font=("Arial", 12), bg="#2196F3", fg="blue")
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear Chat", command=self.clear_conversation, 
                                     width=15, font=("Arial", 12), bg="#f44336", fg="blue")
        self.clear_button.pack(side=tk.LEFT, padx=5)
    
    def append_to_conversation(self, text, is_user=True):
        self.conversation_text.config(state=tk.NORMAL)
        if is_user:
            self.conversation_text.insert(tk.END, "You: ", "user")
            self.conversation_text.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
        else:
            self.conversation_text.insert(tk.END, f"{self.current_model.capitalize()}: ", "ai")
            self.conversation_text.tag_config("ai", foreground="green", font=("Arial", 12, "bold"))
        
        self.conversation_text.insert(tk.END, f"{text}\n\n")
        self.conversation_text.see(tk.END)
        self.conversation_text.config(state=tk.DISABLED)
    
    def record_audio(self):
        # Disable the button during recording
        self.record_button.config(state=tk.DISABLED, text="Recording...")
        self.root.update()
        
        # Open microphone selection dialog
        microphone_dialog = tk.Toplevel(self.root)
        microphone_dialog.title("Select Microphone")
        microphone_dialog.geometry("400x300")
        
        # List available microphones
        mics = self.audio_manager.list_microphones()
        
        listbox = tk.Listbox(microphone_dialog, font=("Arial", 12))
        for mic in mics:
            listbox.insert(tk.END, f"{mic['index']}: {mic['name']}")
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def select_mic():
            try:
                selected_index = int(listbox.get(listbox.curselection()[0]).split(':')[0])
                microphone_dialog.destroy()
                # Start recording in a separate thread
                threading.Thread(target=self.start_recording_thread, args=(selected_index,)).start()
            except IndexError:
                tk.messagebox.showerror("Error", "Please select a microphone")
        
        select_button = tk.Button(microphone_dialog, text="Select", command=select_mic, 
                                 font=("Arial", 12), bg="#4CAF50", fg="blue")
        select_button.pack(pady=10)
    
    def start_recording_thread(self, device_index):
        # Record audio
        wav_file = "user_input.wav"
        self.audio_manager.record_audio(wav_file, duration=5, device_index=device_index)
        
        # Convert speech to text
        text = self.audio_manager.speech_to_text(wav_file)
        
        # Update UI in the main thread
        self.root.after(0, lambda: self.process_speech_result(text))
    
    def process_speech_result(self, text):
        if text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", text)
            self.process_text_input()
        else:
            tk.messagebox.showinfo("Info", "Could not recognize speech. Please try again.")
        
        # Re-enable the record button
        self.record_button.config(state=tk.NORMAL, text="Record Voice")
    
    def process_text_input(self):
        user_text = self.input_text.get("1.0", tk.END).strip()
        if not user_text:
            return
        
        # Display user message
        self.append_to_conversation(user_text, is_user=True)
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Process with LLM in a separate thread
        threading.Thread(target=self.process_llm_response, args=(user_text,)).start()
    
    def process_llm_response(self, user_text):
        # Get response from LLM
        response = self.text_processor.get_response(user_text, model_name=self.current_model)
        
        # Update UI in the main thread
        self.root.after(0, lambda: self.handle_llm_response(response))
    
    def handle_llm_response(self, response):
        # Display AI response
        self.append_to_conversation(response, is_user=False)
        
        # Update cat animation based on the model
        self.cat_animation.change_cat_image(self.current_model)
        
        # Speak the response
        self.text_processor.speak(response, f"response_{self.current_model}.mp3")
    
    def change_model(self, selection):
        self.current_model = selection
        self.cat_animation.change_cat_image(selection)
    
    def clear_conversation(self):
        self.conversation_text.config(state=tk.NORMAL)
        self.conversation_text.delete("1.0", tk.END)
        self.conversation_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()