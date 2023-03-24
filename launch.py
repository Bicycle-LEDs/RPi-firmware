import os, sys
from colorama import init, Fore, Style
script_dir=os.path.dirname(os.path.realpath(__file__))
init()

infoMsg = Fore.GREEN + "[LAUNCH] " + Style.RESET_ALL

print(infoMsg + " Tak będą wyglądać informacje")
print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " Tak ostrzeżenia")
print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " A tak błędy")

# Update
if not len(sys.argv) > 1:
    print(infoMsg + " Aktualizowanie używając polecenia " + Fore.YELLOW + "git pull")
    print()
    print("----------" + Style.RESET_ALL)
    os.system('git pull')
    print(Fore.YELLOW + "----------")
    print()

# Run
print(infoMsg + " Uruchamianie " + Fore.YELLOW + "main.py")
print(" ")

os.system(F'python {script_dir}/app/main.py 2>/dev/null')