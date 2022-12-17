# OpenAI-GUI
**OpenAI based model GUI tool which displays a desktop prompt window for OpenAI GPT3**

The program works. If you encounter problems running it or have other bug reports or features that you wish to see implemented, please fork the project and submit a pull request and/or file an [issue](https://github.com/MaxSSD/OpenAI-GUI/issues) on this project.

# Screenshots & Videos
![Capture](https://user-images.githubusercontent.com/86234226/206861632-620e85da-d41d-44e2-ae06-bdf68ef8ab91.PNG)
*openaigui.py
![PYSimpleopenai](https://user-images.githubusercontent.com/86234226/208240516-02b90a7a-3133-4ae6-bbdc-7f738ced4a96.PNG)
*openaipysgui.py

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
* Start the editor and run the code.

# [Keyboard Shortcuts]
| Key Combo                 | Effect                                             |
| ------------------------- | -------------------------------------------------- |
| Enter                     | Speak                                              |
| Esc                       | Quit                                               |
| Delete                    | Delete text                                        |


# Use ase
Prompt can be input into the GUI then loaded for easy automation of GPT3 model queries to text files on desktop.

## Example/test command
Give 10 ideas for python automation implementations.

# Developer Information
## Known Working Versions of Dependencies for openaigui.py
* openai==0.16.0
* pyttsx3==2.90
* tk==0.1.0
* Pillow==9.2.0
## Known Working Versions of Dependencies for openaipysgui.py
* openai==0.16.0
* pyttsx3==2.90
* PySimpleGUI==4.60.4

## Developing a New Component
* File an issue on GitHub if you need help fitting your OpenAI-GUI into our component system; we would be happy to collaborate

# License
Source code of OpenAI-GUI is licensed under the MIT license.

Some dependencies of this application are under the GPL license. When packaged with these dependencies, OpenAI-GUI may also be under the terms of this GPL license.
