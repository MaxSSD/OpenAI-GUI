import pyttsx3
from PIL import Image

# ERROR RESPONSE VOICE COMMANDS
noacc = "Too many characters, printing in file"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 135)
