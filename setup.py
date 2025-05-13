import tkinter as tk
from tkinter import messagebox
import os
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        "ollama", 
        "pillow", 
        "sounddevice", 
        "SpeechRecognition", 
        "gtts"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def create_directory_structure():
    """Create the necessary directory structure for the application"""
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created 'images' directory")

def install_dependencies(packages):
    """Install missing dependencies"""
    import subprocess
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All dependencies installed successfully!")

def main():
    # Check if all required dependencies are installed
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"Missing dependencies: {', '.join(missing_packages)}")
        
        # Create a simple GUI to ask user if they want to install dependencies
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askyesno(
            "Missing Dependencies",
            f"The following dependencies are missing:\n"
            f"{', '.join(missing_packages)}\n\n"
            f"Do you want to install them now?"
        )
        
        if result:
            install_dependencies(missing_packages)
        else:
            print("Please install the required dependencies and try again.")
            sys.exit(1)
    
    # Create necessary directories
    create_directory_structure()
    
    # Import and run the main application
    try:
        from main import MainApplication
        
        root = tk.Tk()
        app = MainApplication(root)
        root.mainloop()
    
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while starting the application:\n{str(e)}"
        )
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()