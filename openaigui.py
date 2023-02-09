import logging
import PySimpleGUI as sg
import openai
import os
import sys
import requests
import urllib.request
from PIL import Image
from io import BytesIO
from api_key import key
from imgnsound import icon

# @https://beta.openai.com/docs/engines/gpt-3
key = openai.api_key

logger = logging.getLogger()
logging.basicConfig(filename='answers.txt', level=logging.INFO)

# max_tokens_list = (256, 8000)
max_tokens_list = [256, 3999, 7999]
models = ("text-davinci-003", "text-davinci-002",
          "text-curie-001", "text-babbage-001", "text-ada-001")
size_list = ("256x256", "512x512", "1024x1024")

# Defines the modules() and openAi() functions which are used to select the engine and generate a response.


def modules(engines):
    return engines if engines in models else ValueError(f"Invalid engine: {engines}. Must be one of {models}")


def select_max_tokens(max_tokens):
    return max_tokens if max_tokens in max_tokens_list else ValueError(f"Invalid max_tokens: {max_tokens}. Must be one of {max_tokens_list}")


def picture_size(size):
    return size if size in size_list else ValueError(f"Invalid max_tokens: {size}. Must be one of {size_list}")


def openAi(prompt_in, engines, max_tokens):
    sg.popup_quick_message('Responding...')
    completion = openai.Completion.create(engine=modules(
        engines), prompt=prompt_in, temperature=0, max_tokens=select_max_tokens(max_tokens))
    result = completion.choices[0].text
    if len(result) < 150:
        print(result)
        logger.info(result)
    else:
        sg.popup_quick_message('Responding to answers.txt')
        print(result)
        with open('answers.txt', 'a+') as f:
            f.write(result)
    sg.clipboard_set(result)


def dalle(prompt_ins, size):
    response = openai.Image.create(
        prompt=prompt_ins,
        n=1,
        size=picture_size(size)
    )
    image_url = response['data'][0]['url']
    webUrl = urllib.request.urlopen(image_url)
    img = Image.open(webUrl)
    sg.Popup('Displaying and saving image...', keep_on_top=True)
    file_name = os.path.basename(prompt_ins)[:255] + '.png'
    img.show()
    img.save(file_name)


def make_window(theme):
    sg.theme(theme)
    # GUI layout.
    layout = [
        [sg.Text("OpenAIGUI",  expand_x=True, justification="center",
                 font=("Helvetica", 13), relief=sg.RELIEF_RIDGE)],
        [sg.TabGroup([[
            sg.Tab("OpenAi", [
                [sg.Radio("Choose model", "RADIO1", default=True, key="modules"), sg.Combo(
                    models, default_value=models[0], key="-ENGINES-", readonly=True)],
                [sg.Radio("Choose max token", "RADIO1", key="select_max_tokens"), sg.Combo(
                    max_tokens_list, default_value=max_tokens_list[0], key="-MAXTOKENS-", readonly=True)],
                [sg.Text("Enter your question or statement below:",
                         font=('_ 13'))],
                [sg.Pane([sg.Column([[sg.Multiline(key="prompt", size=(77, 20), expand_x=True, expand_y=True, enter_submits=True, focus=True)]]),
                          sg.Column([[sg.Multiline(size=(60, 15), key="-OUTPUT-", font=("Arial", 9), expand_x=True, expand_y=True, write_only=True,
                                                   reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]])], expand_x=True, expand_y=True)],
                [sg.Button("Answer", bind_return_key=True), sg.Button('Open file'), sg.Button("Clear"), sg.Button("Quit")]]),
            sg.Tab("Dall-E", [
                [sg.Text("Suggest impression:", font=("Arial", 9, 'bold'))],
                [sg.Radio("Choose picture size", "RADIO1", key="picture_size"), sg.Combo(
                    size_list, key="-SIZE-")],
                [sg.Multiline(key="promptdalle", size=(
                    77, 20), expand_x=True, expand_y=True)],
                [sg.Button("Create image"), sg.Button("Clear"), sg.Button("Quit")]]),
            sg.Tab("Theme", [
                [sg.Text("Choose theme:")],
                [sg.Listbox(values=sg.theme_list(), size=(
                    20, 12), key="-THEME LISTBOX-", enable_events=True)],
                [sg.Button("Set Theme")]]),
            sg.Tab("About", [
                [sg.Text(
                    "text-davinci-003 - Upgraded davinci-002. GPT3 chatbot model.")],
                [sg.Text(
                    "text-davinci-002 - Code review, complex intent, cause and effect, summarization for audience")],
                [sg.Text(
                    "code-davinci-edit-001 - Edit endpoint is particularly useful for editing code.")],
                [sg.Text(
                    "text-curie-001 - Language translation, complex classification, text sentiment, summarization")],
                [sg.Text(
                    "text-babbage-001 - Moderate classification, semantic search classification")],
                [sg.Text(
                    "text-ada-001 - Parsing text, simple classification, address correction, keywords")]])]], key="-TAB GROUP-", expand_x=True, expand_y=True),
         sg.Sizegrip()]]
    # Gui window and layout sizing.
    window = sg.Window('OpenAI GUI', layout, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, icon=icon, finalize=True)
    window.set_min_size(window.size)
    return window


# GUI window that runs the main() function to interact with the user.
def main():
    window = make_window(sg.theme())
    # Event loop.
    while True:
        event, values = window.read(timeout=None)
        if event == sg.WINDOW_CLOSED or event == 'Quit' or event == 'Exit':
            break
        if values is not None:
            engines = values['-ENGINES-'] if values['-ENGINES-'] == 'Choose model' else values['-ENGINES-']
        if values is not None:
            max_tokens = values['-MAXTOKENS-'] if values['-MAXTOKENS-'] == 'Choose max token' else values['-MAXTOKENS-']
        if values is not None:
            size = values['-SIZE-'] if values['-SIZE-'] == 'Choose picture size' else values['-SIZE-']
        if event == 'Answer':
            prompt_in = values['prompt'].rstrip()
            window['prompt'].update(prompt_in)
            window['-OUTPUT-'].update('')
            openAi(prompt_in, engines, max_tokens)
        elif event == 'Create image':
            prompt_ins = values['promptdalle']
            dalle(prompt_ins, size)
        elif event == 'Open file':
            os.startfile('answers.txt', 'open')
        elif event == 'Clear':
            window['prompt'].update('')
            window["-OUTPUT-"].update('')
        elif event == "Set Theme":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
            sg.user_settings_set_entry('-theme-', theme_chosen)
            sg.popup(f"Chosen Theme: {str(theme_chosen)}", keep_on_top=True)

        if event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(
            ), location=window.current_location(), keep_on_top=True, non_blocking=True)

    window.close()
    sys.exit(0)


if __name__ == '__main__':
    sg.theme(sg.user_settings_get_entry('-theme-', 'dark green 7'))
    main()
