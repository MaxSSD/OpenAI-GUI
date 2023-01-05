import logging
import PySimpleGUI as sg
import openai
from api_key import key
from imgnsound import noacc, speak


# @https://beta.openai.com/docs/engines/gpt-3

# Defines the modules() and openAi() functions which are used to select the engine and generate a response.
def modules(engines):
    if engines == "text-davinci-003":
        m = "text-davinci-003"
    elif engines == "text-davinci-002":
        m = "text-davinci-002"
    elif engines == "text-curie-001":
        m = "text-curie-001"
    elif engines == "text-babbage-001":
        m = "text-babbage-001"
    elif engines == "text-ada-001":
        m = "text-ada-001"
    return m

def openAi(engines, prompt_in):
    # Use the selected module in the engine parameter to choose AI engine.
    completion = openai.Completion.create(engine=modules(engines), prompt=prompt_in, temperature=0, max_tokens=377,
                                         top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
    result = completion.choices[0].text
    length = ((result).join(result)).count(result) + 1
    # Creating an object response
    logger = logging.getLogger()
    logging.basicConfig(filename='answers.txt', level=logging.INFO)
    # Condition to respond with audio or in file.
    if length < 150:
        sg.Popup('Responding...', keep_on_top=True)
        speak(result)
        logger.info(result)
    else:
        sg.Popup('Responding to answer.txt', keep_on_top=True)
        speak(noacc)
        logger.info(result)

def make_window(theme):
    sg.theme(theme)
    # GUI layout.
    layout_prompt = [[sg.Radio('Choose model', 'RADIO1', key='modules'),
                      sg.Combo(['text-davinci-003', 'text-davinci-002', 'text-curie-001', 'text-babbage-001',
                                'text-ada-001'], key='engines')],
                     [sg.Text('Enter your question or statement below:', font=("Arial", 9, 'bold'))],
                     [sg.Multiline(key="prompt", size=(77, 20))],
                     # [sg.Input(key='prompt', size=(77, 1), do_not_clear=True)],
                     [sg.Button('Answer'), sg.Button('Clear'), sg.Button('Quit')]]

    layout_theme = [[sg.Text('Choose theme:')],
                    [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-THEME LISTBOX-', enable_events=True)],
                    [sg.Button("Set Theme")]]

    layout_about = [[sg.Text('text-davinci-003 - Upgraded davinci-002. GPT3 chatbot model.')],
                    [sg.Text('text-davinci-002 - Complex intent, cause and effect, summarization for audience')],
                    [sg.Text('text-curie-001 - Language translation, complex classification, text sentiment, summarization')],
                    [sg.Text('text-babbage-001 - Moderate classification, semantic search classification')],
                    [sg.Text('text-ada-001 - Parsing text, simple classification, address correction, keywords')]]
    # Layout sizing.
    layout = [[sg.Text('OpenAIGUI', size=(63, 1), justification='center', font=("Helvetica", 13),
                       relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]

    layout += [[sg.TabGroup([[sg.Tab('OpenAi', layout_prompt),
                              sg.Tab('Theme', layout_theme),
                              sg.Tab('About', layout_about)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True)]]
    layout[-1].append(sg.Sizegrip())

    # Gui window and layout sizing.
    window = sg.Window('OpenAI GUI', layout, resizable=True, return_keyboard_events=True, use_custom_titlebar=True, finalize=True, keep_on_top=True)
    # window.bind(bind_string="<Enter>", key="Answer", propagate=True)
    return window

# GUI window that runs the main() function to interact with the user.
def main():
    window = make_window(sg.theme())

    # Set keyboard shortcuts for the buttons [ADD KEY BINDS]
    # window['Answer'].bind('<Return>', 'Answer')
    # window['Clear'].bind('<Delete>', 'Clear')
    # window['Quit'].bind('<Escape>', close_me)

    # Event loop.
    while True:
        event, values = window.read(timeout=100)
        if values is not None:
            engines = values['engines'] if values['engines'] == 'Choose model' else values['engines']
        if event == 'Answer':
            prompt_in = values['prompt']
            openAi(engines, prompt_in)
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
