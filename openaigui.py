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

logger = logging.getLogger()
logging.basicConfig(filename='answers.txt', level=logging.INFO)

max_tokens_list = (256, 2000, 8000)
models = ("text-davinci-003", "text-davinci-002", "code-davinci-002",
          "code-cushman-001", "text-curie-001", "text-babbage-001", "text-ada-001")
size_list = ("256x256", "512x512", "1024x1024")

# Defines the modules() and openAi() functions which are used to select the engine and generate a response.
def modules(engines):
    return engines if engines in models else None


def select_max_tokens(max_tokens):
    return max_tokens if max_tokens in max_tokens_list else None


def picture_size(size):
    return size if size in size_list else None


def openAi(prompt_in, engines, max_tokens):
    sg.popup_quick_message('Responding...')
    max_tokens = select_max_tokens(256)
    completion = openai.Completion.create(engine=modules(engines), prompt=prompt_in, temperature=0, max_tokens=select_max_tokens(max_tokens), top_p=1.0)
    result = completion.choices[0].text
    if len(result) < 150:
        print(result)
        logger.info(result)
    else:
        sg.popup_quick_message('Responding to answers.txt')
        print(result)
        with open('answers.txt', 'a+') as f:
            f.write(result)


def dalle(prompt_ins, size):
    sg.popup_quick_message('Creating and saving image...')
    response = openai.Image.create(
        prompt=prompt_ins,
        n=1,
        size=picture_size(size)
    )
    image_url = response['data'][0]['url']
    webUrl = urllib.request.urlopen(image_url)
    img = Image.open(webUrl)
    file_name = os.path.basename(prompt_ins)[:255] + '.png'
    img.show()
    img.save(file_name)


def make_window(theme):
    sg.theme(theme)
    max_tokens = select_max_tokens(256)
    # GUI layout.
    layout = [
        [sg.Text("OpenAIGUI", size=(63, 1), expand_x=True, justification="center", font=("Helvetica", 13), relief=sg.RELIEF_RIDGE)],
        [sg.TabGroup([
            [sg.Tab("OpenAi", [
                [sg.Radio("Choose model", "RADIO1", default=True, key="modules"), sg.Combo(models, default_value=models[0], key="engines", readonly=True)],
                [sg.Radio("Choose max token", "RADIO1", key="select_max_tokens"), sg.Combo(max_tokens_list, default_value=max_tokens_list[0], key="max_tokens")],
                [sg.Text("Enter your question or statement below:",font=("Arial", 9, 'bold'))],
                [sg.Pane([sg.Column([[sg.Multiline(key="prompt", size=(77, 20), expand_x=True, expand_y=True, enter_submits=True, focus=True)]]),
                          sg.Column([[sg.Multiline(size=(60, 15), key="output", font=("Arial", 9), expand_x=True, expand_y=True, write_only=True,
                                                   reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]])], expand_x=True, expand_y=True)],
                [sg.Button("Answer", bind_return_key=True), sg.Button('Open file'),
                 sg.Button("Clear"), sg.Button("Quit")]
            ]),
                sg.Tab("Dall-E", [
                    [sg.Text("Suggest impression:", font=("Arial", 9, 'bold'))],
                    [sg.Radio("Choose picture size", "RADIO1", key="picture_size"), sg.Combo(size_list, default_value=size_list[0], key="size")],
                    [sg.Multiline(key="promptdalle", size=(77, 20), expand_x=True, expand_y=True, enter_submits=True, focus=True)],
                    # Display image in frame [sg.Image(filename=file_name)],
                    # Bind "Create image" to Return key in tab
                    [sg.Button("Create image"), sg.Button(
                        "Clear"), sg.Button("Quit")]
                ]),
                sg.Tab("Theme", [
                    [sg.Text("Choose theme:")],
                    [sg.Listbox(values=sg.theme_list(), size=(20, 12),key="-THEME LISTBOX-", enable_events=True)],
                    [sg.Button("Set Theme")]
                ]),
                sg.Tab("About", [
                    [sg.Text(
                        "text-davinci-003 - Upgraded davinci-002. GPT3 chatbot model.")],
                    [sg.Text(
                        "text-davinci-002 - Code review, complex intent, cause and effect, summarization for audience")],
                    [sg.Text("code-davinci-002 - Most capable Codex model. Particularly good at translating natural language to code. In addition to completing code, also supports inserting completions within code.")],
                    [sg.Text("code-cushman-001 - Almost as capable as Davinci Codex, but slightly faster. This speed advantage may make it preferable for real-time applications.")],
                    [sg.Text(
                        "text-curie-001 - Language translation, complex classification, text sentiment, summarization")],
                    [sg.Text(
                        "text-babbage-001 - Moderate classification, semantic search classification")],
                    [sg.Text(
                        "text-ada-001 - Parsing text, simple classification, address correction, keywords")]
                ])
            ]], key="-TAB GROUP-", expand_x=True, expand_y=True), sg.Sizegrip()]]
    # Gui window and layout sizing.
    window = sg.Window('OpenAI GUI', layout, resizable=True, return_keyboard_events=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, icon=icon)
    return window


# GUI window that runs the main() function to interact with the user.
def main():
    window = make_window(sg.theme())
    # Event loop.
    while True:
        event, values = window.read(timeout=100)
        max_tokens = select_max_tokens(377)
        if values is not None:
            engines = values['engines'] if values['engines'] == 'Choose model' else values['engines']
        if values is not None:
            max_tokens = values['max_tokens'] if values['max_tokens'] == 'Choose max token' else values['max_tokens']
        if values is not None:
            size = values['size'] if values['size'] == 'Choose picture size' else values['size']
        if event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(
            ), location=window.current_location(), keep_on_top=True, non_blocking=True)
        elif event == 'Answer':
            prompt_in = values['prompt']
            openAi(prompt_in, engines, max_tokens)
        elif event == 'Create image':
            prompt_ins = values['promptdalle']
            dalle(prompt_ins, size)
        elif event == 'Open file':
            os.startfile('answers.txt', 'open')
        elif event == 'Clear':
            window['prompt'].update('')
            window['output'].update('')
        elif event == "Set Theme":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
            sg.popup(f"Chosen Theme: {str(theme_chosen)}", keep_on_top=True)
        elif event == sg.WINDOW_CLOSED or event == 'Quit':
            break

    window.close()
    sys.exit(0)


if __name__ == '__main__':
    sg.theme('black')
    sg.theme('dark red')
    sg.theme('dark green 7')
    main()
