import openai
import pyttsx3
from PIL import Image, ImageWin
from tkinter import Tk,Frame,Label,Button,Entry,Text,StringVar,mainloop
from resizeimage import resizeimage

# API KEY
openai.api_key = "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"

# AI ENGINE TYPES
#engines = openai.Engine.list()
"""
print the first engine's id
print(engines.data[0].id)
"""
""" @https://beta.openai.com/docs/engines/gpt-3
text-davinci-002 <--- Complex intent, cause and effect, summarization for audience
text-curie-001 <---  Language translation, complex classification, text sentiment, summarization
text-babbage-001 <--- Moderate classification, semantic search classification
text-ada-001 <--- Parsing text, simple classification, address correction, keywords
"""
# Codex
""" @https://beta.openai.com/docs/engines/codex-series-private-beta
code-davinci-002 <--- Completions within code
cide-cushman-001 <--- Faster completion
"""

# GUI SPECIFICATION
me = Tk()
me.title('OpenAI GUI')
me.geometry("500x125")
me.resizable(True,True)

# GUI FRAME
frame = Frame(me, background='Black')
frame.grid(sticky= "NSEW")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

me.grid_rowconfigure(0,weight=1)
me.grid_columnconfigure(0,weight=1)

# USER INPUT
prompt_in = StringVar()
message = StringVar()

#GUI LABEL
delabel=Label(frame, text="PRESS: Enter to Speak; Esc to Quit; Delete to Delete text", bg='Black',fg='White',font=("Arial",9, 'bold'))
melabel=Label(frame, text="OpenAI", bg='Black',fg='White',font=("Arial",18, 'bold'))

delabel.grid(row=1, column=0, sticky="NSEW")
melabel.grid(row=3, column=0, sticky= "NSEW")

melabel.grid_rowconfigure(1, weight=1)
melabel.grid_columnconfigure(1, weight=1)
delabel.grid_rowconfigure(5, weight=1)
delabel.grid_columnconfigure(5, weight=1)

# AI SOUL
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 135)

# TEXT2SPEECH MODULE
def speak(audio):
    # print(audio)
    engine.say(audio)
    engine.runAndWait()

# ERROR RESPONSE COMMANDS
noacc = "Too many characters, printing in console"

# API DOCUMENTATION FILE
def openAi():
    command = prompt_in.get()
    prompt_in.set(command)
    completion = openai.Completion.create(engine="text-davinci-002", prompt=command,
                                          temperature=0,
                                          max_tokens=204,
                                          top_p=1.0,
                                          frequency_penalty=0.0,
                                          presence_penalty=0.0
                                          )
    result = completion.choices[0].text
    length = ((result).join(result)).count(result) + 1
    if length < 150:
        print(result)
        speak(result)
    else:
        speak(noacc)
        print(result)

# DISPLAY PHOTOS REQUESTED
def displaypng():
    display = resizeimage.resize_cover(qr_code, [180, 180])
    img = ImageTk.PhotoImage(display)

# CLEAR PROMPT
def clr():
    prompt_in.set('')

# SAVE TO FILE
def extract_data():
    command = prompt_in.get()
    prompt_in.set(command)
    completion = openai.Completion.create(engine="text-davinci-002", prompt=command)
    print(completion.choices[0].text)

# GUI FUNCTIONS
but_choice=Button(me, text="Speak", bg='Black',fg='White', command=openAi,font=("Arial",15,'bold'))
but_clear=Button(me, text='Clear', bg='Black', fg='White', command=clr, font=("Arial",15,'bold'))

txt_input = Entry(me, textvar=prompt_in, bg='White', fg='Black', font=("Arial",12,'bold'))
# text_output = Text(me, text=message, bg='White', fg='Black', font=("Arial",12,'bold'))

#GUI FUNCTIONS CSS
but_choice.grid(row=7, column=0, sticky="we")
#but_clear.grid(rows=9, column=0, sticky="we")

txt_input.grid(row=5, column=0, sticky="we")
#text_output.grid(row=14, column=0, sticky="we")

# BUTTON BIND
def enter(event=[openAi,clr]):
    but_choice['command'] = openAi
    but_clear['command'] = clr

# CLOSE WINDOW
def close_me(e):
    me.destroy()

me.bind('<Return>', lambda enter: but_choice.invoke())
me.bind('<Delete>', lambda enter: but_clear.invoke())
me.bind('<Escape>', lambda e: close_me(e))


if __name__ == '__main__':
    mainloop()