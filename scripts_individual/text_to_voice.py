from gtts import gTTS
import os

mytext = 'hey this is new text made by umair'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome2.mp3")
os.system("open welcome.mp3")  # Use 'open' instead of 'start' on macOS