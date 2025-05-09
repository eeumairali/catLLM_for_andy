import tkinter as tk
from PIL import Image, ImageTk

class CatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat Viewer")
        self.root.configure(bg="blue")
        self.root.geometry("600x400")

        # List of cat images
        self.cat_images = ["images/cat1.png", "images/cat2.png", "images/cat3.png",
                          "images/cat4.png"]
        self.current_index = 0

        # Load the first image
        self.image_label = tk.Label(self.root, bg="blue")
        self.image_label.pack(expand=True)
        self.load_image()

        # Bind left and right arrow keys
        self.root.bind("<Left>", self.show_previous_image)
        self.root.bind("<Right>", self.show_next_image)

    def load_image(self):
        try:
            image = Image.open(self.cat_images[self.current_index])
            image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Updated here
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            print(f"Error loading image: {e}")

    def show_previous_image(self, event):
        self.current_index = (self.current_index - 1) % len(self.cat_images)
        self.load_image()

    def show_next_image(self, event):
        self.current_index = (self.current_index + 1) % len(self.cat_images)
        self.load_image()