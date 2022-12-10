# OpenAI-GUI
**OpenAI based model GUI tool which displays a desktop prompt window for OpenAI GPT3**

The program works. If you encounter problems running it or have other bug reports or features that you wish to see implemented, please fork the project and submit a pull request and/or file an [issue](https://github.com/MaxSSD/OpenAI-GUI/issues) on this project.


# Screenshots & Videos
TBD

# Installation

## Installation on Windows
* Install Python from the Windows Store
* Add Python to your system PATH (it should ask during the installation process)
* Download this repo (extract from zip if needed)
* Open command prompt, `cd` into the repo directory, and run: `pip install .`
* Download this repository and install it using Pip: `pip3 install .` (or use `pipx` for isolation)
* Add your API key from [https://beta.openai.com/account/api-keys]
* Copy it into the api_key.py file.
* Use the following commands to install the needed dependencies:
```
pip install requirements.txt
```
* Start the app with `run openai` or `python3 -m openaigui.py`

# [Keyboard Shortcuts](https://github.com/djfun/audio-visualizer-python/wiki/Keyboard-Shortcuts)
| Key Combo                 | Effect                                             |
| ------------------------- | -------------------------------------------------- |
| Enter                     | Speak                                              |
| Esc                       | Quit                                               |
| Delete                    | Delete text                                        |


# Commandline Mode
Projects can be created with the GUI then loaded from the commandline for easy automation of GPT3 model prompt queries.

## Example/test command
Give 10 ideas for python automation implementations.


# Developer Information
## Known Working Versions of Dependencies
* openai==0.16.0
* pyttsx3==2.90
* tk==0.1.0
* python-resize-image==1.1.20


## Developing a New Component
* File an issue on GitHub if you need help fitting your OpenAI-GUI into our component system; we would be happy to collaborate


# License
Source code of OpenAI-GUI is licensed under the MIT license.

Some dependencies of this application are under the GPL license. When packaged with these dependencies, OpenAI-GUI may also be under the terms of this GPL license.
