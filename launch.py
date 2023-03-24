import os
from colorama import init, Fore, Style
init()
print(Fore.GREEN + "[INFO]" + Style.RESET_ALL + " Uruchamianie...")

os.system('python ./modules/base/main.py 2>/dev/null')