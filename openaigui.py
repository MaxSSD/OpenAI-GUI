import openai
import pyttsx3
from tkinter import *


openai.api_key = "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"

#Engine Types
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

""" GUI SPECIFICATIONS """
me = Tk()
me.title('OpenAI GUI')
me.geometry("400x100")
me.resizable(True,False)

""" GUI FRAME """
frame = Frame(me, background='Black',relief='sunken')
frame.grid(sticky= "NSEW")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

me.grid_rowconfigure(0,weight=1)
me.grid_columnconfigure(0,weight=1)

""" USER INPUT """
prompt_in = StringVar()

""" AI OUTPUT """
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 135)

""" SUBSTITUTE print() TO speak() """
def speak(audio):
    # print(audio)
    engine.say(audio)
    engine.runAndWait()

""" API SERVICING """
def openAi():
    command = prompt_in.get()
    prompt_in.set(command)
    completion = openai.Completion.create(engine="text-davinci-002", prompt=command)
    speak(completion.choices[0].text)

""" GUI LABEL """
melabel=Label(frame, text="OpenAI", bg='Black',fg='White',font=("Arial",18, 'bold'))
melabel.grid(row=3, column=0,sticky= "NSEW")
melabel.grid_rowconfigure(1, weight=1)
melabel.grid_columnconfigure(1, weight=1)
""" GUI FUNCTIONALITY """
but_choice=Button(me, bg='Black',fg='White',text="Speak",command=openAi,font=("Arial",15,'bold'))
txt_input = Entry(me, textvar=prompt_in, bg='White', fg='Black', font=("Arial",12,'bold'))

""" GUI DESIGN """
but_choice.grid(row=5, column=0, sticky="we")
txt_input.grid(row=4, column=0, sticky="we")

mainloop()