import tkinter as tk
import logging
import openai
from tkinter import ttk, Button, Entry, StringVar, RIDGE, PhotoImage
from PIL import Image
from api_key import key
from imgnsound import count, anim, info, noacc, engine, voices

# Engine Types
# engines = openai.Engine.list()
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

class OpenAIGUI:
    def openAi(self):
        def speak(audio):
            # print(audio)
            engine.say(audio)
            engine.runAndWait

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
        # Creating an object
        logger = logging.getLogger()
        logging.basicConfig(filename='answers.txt', level=logging.INFO)
        if length < 150:
            logger.info(result)
            speak(result)
        else:
            logger.info(result)
            speak(noacc)

    def clr(self):
        self.prompt_in.set('')

    def entertorun(event=[openAi]):
        but_choice['command'] = [openAi]

    def deletetoquit(event=[clr]):
        but_clear['command'] = clr

    def __init__(self, root):
        self.root = root
        self.root.title('OpenAI GUI')
        self.root.geometry("483x616")
        self.root.resizable(False, False)
        style = ttk.Style()
        style.configure('Black.Treeview', background='black')

        # GUI FRAME
        entryframe = ttk.Frame(self.root, relief=RIDGE, style='Black.TLabel')
        entryframe.grid(sticky="NSEW")
        entryframe.configure(style='Black.TLabel')
        entryframe.grid_rowconfigure(1, weight=0)
        entryframe.grid_columnconfigure(1, weight=0)

        # USER INPUT
        self.prompt_in = StringVar()
        self.message = StringVar()

        # GIF ORB [MAKE IT A SPEAKER SOUND VISUALIZER]
        # gives total number of frames that gif contains
        frames = info.n_frames
        # creating list of PhotoImage objects for each frames
        im = [tk.PhotoImage(file='orb.gif', format=f"gif -index {i}") for i in range(frames)]

        # GUI LABEL
        self.delabel = ttk.Label(entryframe, text="Enter to Speak; Esc to Quit; Delete to Delete text",
                                 font=("Arial", 9, 'bold'))
        self.gif_label = ttk.Label(entryframe, image='')

        if info is not None and isinstance(info, PhotoImage):
            self.gif_label.configure(image=info)

        self.delabel.grid(row=3, column=0, sticky="NSEW")
        self.gif_label.grid(row=2, column=0, sticky="N")

        self.delabel.grid_rowconfigure(5, weight=1)
        self.delabel.grid_columnconfigure(5, weight=1)

        self.gif_label.grid_rowconfigure(4, weight=1)
        self.gif_label.grid_columnconfigure(4, weight=1)

        # GUI FUNCTIONALITY
        but_choice = Button(entryframe, bg='Black', fg='White', text="Speak", command=self.openAi,
                            font=("Arial", 15, 'bold'))
        but_clear = Button(entryframe, text='Clear', bg='Black', fg='White', command=self.clr,
                           font=("Arial", 15, 'bold'))
        txt_input = Entry(entryframe, textvar=self.prompt_in, bg='White', fg='Black', font=("Arial", 17, 'bold'))

        # GUI DESIGN
        but_choice.grid(row=6, column=0, sticky="NSWE")
        but_clear.grid(row=7, column=0, sticky="NSWE")
        txt_input.grid(row=5, column=0, sticky="NSWE")

        # GIF ANIMATION
        def animation(count):
            global anim
            im2 = im[count]

            self.gif_label.configure(image=im2)
            count += 1
            if count == frames:
                count = 0
            anim = root.after(50, lambda: animation(count))

        animation(count)

        """def stop_animation(self):
            root.after_cancel(anim)"""

        # CLOSE WINDOW
        def close_me(e):
            root.destroy()

        root.bind('<Return>', lambda entertorun: but_choice.invoke())
        root.bind('<Delete>', lambda deletetoquit: but_clear.invoke())
        root.bind('<Escape>', lambda e: close_me(e))

if __name__ == '__main__':
    # DEFINE WINDOW
    root = tk.Tk()
    # INITIATE WINDOW
    o = OpenAIGUI(root)
    root.mainloop()
else:
    print('Client exit!')
