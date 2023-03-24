import os, sys
from colorama import init, Fore, Style
import pip
script_dir=os.path.dirname(os.path.realpath(__file__))
init()

infoMsg = Fore.GREEN + "[LAUNCH] " + Style.RESET_ALL

print(infoMsg + " Tak będą wyglądać informacje")
print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " Tak ostrzeżenia")
print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " A tak błędy")
print()

# Update
if not len(sys.argv) > 1:
    print(infoMsg + " Aktualizowanie systemu używając polecenia " + Fore.YELLOW + "yay -Syu")
    print("----------" + Style.RESET_ALL)
    os.system('yay -Syu')
    print(Fore.YELLOW + "----------")
    print()

    print(infoMsg + " Aktualizowanie kodu używając polecenia " + Fore.YELLOW + "git pull")
    print("----------" + Style.RESET_ALL)
    os.system('git pull')
    print(Fore.YELLOW + "----------")
    print()

    print(infoMsg + " Aktualizowanie bibliotek używając polecenia " + Fore.YELLOW + "pip install -U")
    print("----------" + Style.RESET_ALL)
    packages = [dist.project_name for dist in pip.get_installed_distributions()]
    os.system("pip install --upgrade " + ' '.join(packages))
    print(Fore.YELLOW + "----------")
    print()

# Run
print(infoMsg + " Uruchamianie " + Fore.YELLOW + "main.py")

os.system(F'python {script_dir}/app/main.py 2>/dev/null')