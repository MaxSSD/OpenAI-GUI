import openai
import pyttsx3
from tkinter import *


openai.api_key = "APIKEY" #Get your at --> https://beta.openai.com/account/api-keys

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


but_choice.grid(row=5, column=0, sticky="we")
txt_input.grid(row=4, column=0, sticky="we")

mainloop()
