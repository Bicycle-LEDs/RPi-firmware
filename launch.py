import os, sys
from colorama import init, Fore, Style
import pkg_resources
script_dir=os.path.dirname(os.path.realpath(__file__))
init()

infoMsg = Fore.GREEN + "[LAUNCH] " + Style.RESET_ALL
startscriptMsg = Fore.YELLOW + "--------------------" + Style.RESET_ALL
endScriptMsg = Fore.BLUE + "--------------------" + Style.RESET_ALL

print(infoMsg + "Tak będą wyglądać informacje")
print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " Tak ostrzeżenia")
print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " A tak błędy")
print()

# Update
if not len(sys.argv) > 1:
    
    print(infoMsg + "Aktualizowanie systemu używając polecenia " + Fore.YELLOW + "yay -Syu")
    print(startscriptMsg)
    os.system('yay -Syu')
    print(endScriptMsg)
    print()

    print(infoMsg + "Aktualizowanie kodu używając polecenia " + Fore.YELLOW + "git pull")
    print(startscriptMsg)
    os.system('git pull')
    print(endScriptMsg)
    print()

    print(infoMsg + "Aktualizowanie bibliotek używając polecenia " + Fore.YELLOW + "pip install -U")
    print(startscriptMsg)
    packages = [dist.project_name for dist in pkg_resources.working_set]
    os.system("pip install --upgrade " + ' '.join(packages))
    print(endScriptMsg)
    print()

# Run
print(infoMsg + "Uruchamianie " + Fore.YELLOW + "main.py")

os.system(F'python {script_dir}/app/main.py 2>/dev/null')