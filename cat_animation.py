from PIL import Image, ImageTk
import tkinter as tk
import os

class CatAnimation:
    def __init__(self, root):
        self.root = root
        
        # Create image paths
        self.image_paths = {
            "gemma3": "images/cat1.png",
            "llama3": "images/cat2.png",
            "qwen3:0.6b": "images/cat3.png",
            "deepseek-r1:1.5b": "images/cat4.png",
        }
        
        # Ensure the images directory exists
        os.makedirs("images", exist_ok=True)
        
        # Current model
        self.current_model = "gemma3"
        
        # Image display objects
        self.image_label = None
        self.tk_image = None
    
    def setup_in_frame(self, frame):
        """Set up the cat animation in the provided frame"""
        self.image_label = tk.Label(frame, bg="#f0f0f0")
        self.image_label.pack(expand=True)
        self.load_current_image()
    
    def load_current_image(self):
        """Load the image for the current model"""
        try:
            # Check if the image file exists
            image_path = self.image_paths[self.current_model]
            if not os.path.exists(image_path):
                # Create a placeholder image if the actual image doesn't exist
                self.create_placeholder_image(image_path, self.current_model)
            
            # Open and resize the image
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Create a text label if image loading fails
            self.image_label.config(image="", text=f"{self.current_model.upper()} CAT", 
                                   font=("Arial", 24, "bold"), fg="purple")
    
    def change_cat_image(self, model_name):
        """Change the cat image based on the LLM model"""
        if model_name in self.image_paths:
            self.current_model = model_name
            self.load_current_image()
    
    def create_placeholder_image(self, path, model_name):
        """Create a placeholder image if the actual image doesn't exist"""
        try:
            # Create a colored image based on the model
            colors = {
                "gemma3": (255, 100, 100),  # Red-ish
                "llama3": (100, 255, 100),  # Green-ish
                "mistral": (100, 100, 255), # Blue-ish
                "phi3": (255, 255, 100)     # Yellow-ish
            }
            color = colors.get(model_name, (200, 200, 200))
            
            # Create a new image
            img = Image.new('RGB', (300, 300), color=color)
            
            # Save the image
            img.save(path)
            print(f"Created placeholder image for {model_name} at {path}")
        except Exception as e:
            print(f"Error creating placeholder image: {e}")