import PySimpleGUI as sg
import logging
import openai
from api_key import key
from imgnsound import noacc, engine, voices, speak

# @https://beta.openai.com/docs/engines/gpt-3

def modules(engines):
    if engines == "text-davinci-002":
        m = "text-davinci-002"
    elif engines == "text-curie-001":
        m = "text-curie-001"
    elif engines == "text-babbage-001":
        m = "text-babbage-001"
    elif engines == "text-ada-001":
        m = "text-ada-001"
    return m

def openAi(engines, prompt_in):
    # Use the selected module in the engine parameter
    completion = openai.Completion.create(engine=modules(engines), prompt=prompt_in, temperature=0, max_tokens=377,
                                         top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
    result = completion.choices[0].text
    length = ((result).join(result)).count(result) + 1
    # Creating an object
    logger = logging.getLogger()
    logging.basicConfig(filename='answers.txt', level=logging.INFO)
    if length < 150:
        speak(result)
        logger.info(result)
    else:
        speak(noacc)
        logger.info(result)

def make_window():
    # GUI LAYOUT
    layout_d = [
        [sg.Radio('Choose model', 'RADIO1', key='modules'),
         sg.Combo(['text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001'], key='engines')],
        [sg.Text('Enter your question or statement below:', font=("Arial", 9, 'bold'))],
        [sg.Input(key='prompt', size=(70, 1), do_not_clear=True)],
        [sg.Button('Answer'), sg.Button('Quit')]
        # [sg.Multiline(size=(70, 5), key='textbox')]
    ]

    layout = [[sg.Text('OpenAIGUI', size=(63, 1), justification='center', font=("Helvetica", 13),
                       relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]

    layout += [[sg.TabGroup([[sg.Tab('OpenAi', layout_d)]], key='-TAB GROUP-', expand_x=True, expand_y=True)
                ]]
    layout[-1].append(sg.Sizegrip())
    # GUI WINDOW
    window = sg.Window('OpenAI GUI', layout)
    return window

# GUI INTERACTION LOOP
def main():
    window = make_window()
    while True:
        event, values = window.read()
        # Retrieve the selected module from the GUI elements
        engines = values['engines'] if values['engines'] == 'Choose model' else values['engines']
        if event == 'Answer':
            prompt_in = values['prompt']
            sg.Popup('Responded to answer.txt file')
            openAi(engines, prompt_in)
        if event == engines == 'text-davinci-002':
            sg.Popup('Complex intent, cause and effect, summarization for audience')
        if event == engines == 'text-curie-001':
            sg.Popup('Language translation, complex classification, text sentiment, summarization')
        if event == engines == 'text-babbage-001':
            sg.Popup('Moderate classification, semantic search classification')
        if event == engines == 'text-ada-001':
            sg.Popup('Parsing text, simple classification, address correction, keywords')
        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            break
    window.close()
    exit(0)

if __name__ == '__main__':
    sg.theme('black')
    sg.theme('dark red')
    sg.theme('dark green 7')
    main()
