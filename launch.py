import os
from colorama import init, Fore, Style
init()
print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " Tak będą wyglądać ostrzeżenia")
print(Fore.GREEN + "[LAUNCH]" + Style.RESET_ALL + " Tak informacje")
print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " A tak błędy")
print(Fore.GREEN + "[LAUNCH]" + Style.RESET_ALL + " Uruchamianie " + Fore.YELLOW + "main.py")

os.system('python ./app/main.py 2>/dev/null')