import os
from colorama import init, Fore, Style
init()
print(Fore.YELLOW + "Launching..." + Style.RESET_ALL)

os.system('python ./modules/speechRecognition.py 2>/dev/null')