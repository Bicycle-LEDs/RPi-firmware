import os
from colorama import init, Fore, Style
init()
print(Fore.BLUE + "[SYS]" + Style.RESET_ALL + " Uruchamianie...")

os.system('python ./modules/speechRecognition.py 2>/dev/null')