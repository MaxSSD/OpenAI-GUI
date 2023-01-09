import logging
import PySimpleGUI as sg
import openai
import os
import requests
import urllib.request
from PIL import Image
from io import BytesIO
from api_key import key
from imgnsound import noacc, speak


# @https://beta.openai.com/docs/engines/gpt-3

logger = logging.getLogger()
logging.basicConfig(filename='answers.txt', level=logging.INFO)

# Defines the modules() and openAi() functions which are used to select the engine and generate a response.
def modules(engines):
    if engines == "text-davinci-003":
        model = "text-davinci-003"
    elif engines == "text-davinci-002":
        model = "text-davinci-002"
    elif engines == "text-curie-001":
        model = "text-curie-001"
    elif engines == "text-babbage-001":
        model = "text-babbage-001"
    elif engines == "text-ada-001":
        model = "text-ada-001"
    return model

def openAi(prompt_in):
    completion = openai.Completion.create(engine=modules(engines), prompt=prompt_in, temperature=0, max_tokens=377,
                                         top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
    result = completion.choices[0].text
    if len(result) < 150:
        sg.Popup('Responding...', keep_on_top=True)
        speak(result)
        logger.info(result)
    else:
        sg.Popup('Responding to answers.txt', keep_on_top=True)
        speak(noacc)
        with open('answers.txt', 'a+') as f:
            f.write(result)

def dalle(prompt_ins):
    try:
        response = openai.Image.create(
            prompt=prompt_ins,
            n=1,
            size="256x256"
        )
        image_url = response['data'][0]['url']
        webUrl = urllib.request.urlopen(image_url)
        img = Image.open(webUrl)
        speak('Displaying and saving image')
        img.save(f'Dall-E: {prompt_ins}.png')
        img.show()
    except openai.error.OpenAIError as e:
        logging.info(e.http_status)
        logging.info(e.error)
        
def make_window(theme):
    sg.theme(theme)
    # GUI layout.
    layout = [
        [sg.Text("OpenAIGUI", size=(63, 1), justification="center", font=("Helvetica", 13), relief=sg.RELIEF_RIDGE, key="-TEXT HEADING-", enable_events=True)],
        [sg.TabGroup([
            [sg.Tab("OpenAi", [
                [sg.Radio("Choose model", "RADIO1", key="modules"), sg.Combo(["text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"],key="engines")],
                [sg.Text("Enter your question or statement below:", font=("Arial", 9, 'bold'))],
                [sg.Multiline(key="prompt", size=(77, 20))],
                [sg.Button("Answer"), sg.Button('Open file'), sg.Button("Clear"), sg.Button("Quit")]
            ]),
             sg.Tab("Dall-E", [
                 [sg.Text("Suggest impression:", font=("Arial", 9, 'bold'))],
                 [sg.Multiline(key="promptdalle", size=(77, 20))],
                 [sg.Button("Create image"), sg.Button("Clear"), sg.Button("Quit")]
             ]),
            sg.Tab("Theme", [
                [sg.Text("Choose theme:")],
                [sg.Listbox(values=sg.theme_list(), size=(20, 12), key="-THEME LISTBOX-", enable_events=True)],
                [sg.Button("Set Theme")]
            ]),
            sg.Tab("About", [
                [sg.Text("text-davinci-003 - Upgraded davinci-002. GPT3 chatbot model.")],
                [sg.Text("text-davinci-002 - Complex intent, cause and effect, summarization for audience")],
                [sg.Text("text-curie-001 - Language translation, complex classification, text sentiment, summarization")],
                [sg.Text("text-babbage-001 - Moderate classification, semantic search classification")],
                [sg.Text("text-ada-001 - Parsing text, simple classification, address correction, keywords")]
            ])
        ]], key="-TAB GROUP-", expand_x=True, expand_y=True)
    ]]
    layout[-1].append(sg.Sizegrip())
    # Gui window and layout sizing.
    # icon='C:/OpenAI-GUI/icon.ico'
    window = sg.Window('OpenAI GUI', layout, resizable=True, return_keyboard_events=True, finalize=True)
    # window.bind(bind_string="<Enter>", key="Answer", propagate=True)
    # window.bind('<Configure>', "Configure")
    return window

# GUI window that runs the main() function to interact with the user.
def main():
    window = make_window(sg.theme())   
    # Event loop.
    while True:
        event, values = window.read(timeout=100)
        if values is not None:
            engines = values['engines'] if values['engines'] == 'Choose model' else values['engines']
        if event == 'Answer':
            prompt_in = values['prompt']
            openAi(prompt_in)
        elif event == 'Create image':
            prompt_ins = values['promptdalle']
            dalle(prompt_ins)
        elif event == 'Open file':
            os.startfile('answers.txt', 'open')
        elif event == 'Clear':
            window['prompt'].update('')
        elif event == "Set Theme":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
            sg.popup(f"Chosen Theme: {str(theme_chosen)}", keep_on_top=True)
        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            break

    window.close()
    exit(0)

if __name__ == '__main__':
    sg.theme('black')
    sg.theme('dark red')
    sg.theme('dark green 7')
    main()
    
