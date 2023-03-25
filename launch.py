import os, sys
from colorama import init, Fore, Style
import pkg_resources
script_dir=os.path.dirname(os.path.realpath(__file__))
init()

print()
infoMsg = Fore.GREEN + "[LAUNCH] " + Style.RESET_ALL
startscriptMsg = Fore.YELLOW + "--------------------" + Style.RESET_ALL
endScriptMsg = Fore.BLUE + "--------------------" + Style.RESET_ALL

print(infoMsg + "Tak będą wyglądać informacje,")
print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " tak ostrzeżenia,")
print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " a tak błędy.")
print(infoMsg + "(TTS) Czytane wiadomości będą miały oznaczenie TTS - text to speech.")
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
    os.system(F'cd {script_dir}&& git pull')
    print(endScriptMsg)
    print()

    print(infoMsg + "Aktualizowanie bibliotek używając polecenia " + Fore.YELLOW + "pip install -U")
    print(startscriptMsg)
    packages = [dist.project_name for dist in pkg_resources.working_set]
    os.system("sudo pip install --upgrade " + ' '.join(packages))
    print(endScriptMsg)
    print()

# Run
print(infoMsg + "Uruchamianie programu - " + Fore.YELLOW + "main.py")
print(startscriptMsg)

os.system(F'sudo python {script_dir}/app/main.py 2>/dev/null')
print(endScriptMsg)