import openai
import pyttsx3
import tkinter as tk
from tkinter import ttk, Button, Entry, StringVar, RIDGE
from api_key import key

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

class OpenAIGUI:
    def openAi(self):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 135)

        def speak(audio):
            # print(audio)
            engine.say(audio)
            engine.runAndWait()

        command = self.prompt_in.get()
        self.prompt_in.set(command)
        completion = openai.Completion.create(engine="text-davinci-002", prompt=command,
                                              temperature=0,
                                              max_tokens=4000,
                                              top_p=1.0,
                                              frequency_penalty=0.0,
                                              presence_penalty=0.0
                                              )
        result = completion.choices[0].text
        length = ((result).join(result)).count(result) + 1
        with open("answers.txt", "a") as file:
            file.write(command + '')
            file.write(result + '')
        if length < 150:
            print(result)
            speak(result)
        else:
            speak(noacc)
            print(result)

    def entertorun(event=[openAi]):
        but_choice['command'] = openAi

    def clr(self):
        self.prompt_in.set('')

    def deletetoquit(event=[clr]):
        but_clear['command'] = clr

    def __init__(self, root):
        self.root = root
        self.root.title('OpenAI GUI')
        self.root.geometry("273x167")
        self.root.resizable(False, False)
        style = ttk.Style()
        style.configure('Black.Treeview', background='black')

        # GUI FRAME
        entryframe = ttk.Frame(self.root, relief=RIDGE, style='Black.TLabel')
        entryframe.grid(sticky="NSEW")
        entryframe.configure(style='Black.TLabel')
        entryframe.grid_rowconfigure(10, weight=10)
        entryframe.grid_columnconfigure(10, weight=10)

        # USER INPUT
        self.prompt_in = StringVar()
        self.message = StringVar()

        # GUI LABEL
        self.delabel = ttk.Label(entryframe, text="Enter to Speak; Esc to Quit; Delete to Delete text", font=("Arial", 9, 'bold'))
        self.melabel = ttk.Label(entryframe, text="OpenAI GUI 0.1", font=("Arial", 18, 'bold'))

        self.delabel.grid(row=3, column=0, sticky="NSEW")
        self.melabel.grid(row=2, column=0, sticky="NSEW")

        self.delabel.grid_rowconfigure(5, weight=1)
        self.delabel.grid_columnconfigure(5, weight=1)
        self.melabel.grid_rowconfigure(1, weight=1)
        self.melabel.grid_columnconfigure(1, weight=1)


        # GUI FUNCTIONALITY
        but_choice = Button(entryframe, bg='Black', fg='White', text="Speak", command=self.openAi, font=("Arial", 15, 'bold'))
        but_clear = Button(entryframe, text='Clear', bg='Black', fg='White', command=self.clr, font=("Arial", 15, 'bold'))

        txt_input = Entry(entryframe, textvar=self.prompt_in, bg='White', fg='Black', font=("Arial", 17, 'bold'))
        # text_output = Text(root, text=message, bg='White', fg='Black', font=("Arial",12,'bold'))

        #GUI DESIGN
        but_choice.grid(row=6, column=0, sticky="NSWE")
        but_clear.grid(row=7, column=0, sticky="NSWE")

        txt_input.grid(row=5, column=0, sticky="WE")

        # CLOSE WINDOW
        def close_me(e):
            root.destroy()

        root.bind('<Return>', lambda entertorun: but_choice.invoke())
        root.bind('<Delete>', lambda deletetoquit: but_clear.invoke())
        root.bind('<Escape>', lambda e: close_me(e))


if __name__ == '__main__':
    # ERROR RESPONSE VOICE COMMANDS
    noacc = "Too many characters, printing in file"
    # DEFINE WINDOW
    root = tk.Tk()
    # INITIATE WINDOW
    o = OpenAIGUI(root)
    root.mainloop()
else:
    print('Client exit!')
