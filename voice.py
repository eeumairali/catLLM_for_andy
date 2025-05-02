from gtts import gTTS
import os

mytext = 'East or west andy I am the best'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")
os.system("open welcome.mp3")  # Use 'open' instead of 'start' on macOS