import os, sys
from colorama import init, Fore, Style
script_dir=os.path.dirname(os.path.realpath(__file__))
init()

# Launch
if len(sys.argv) > 1 and sys.argv[1] == 'launch':

    print(Fore.GREEN + "[LAUNCH]" + Style.RESET_ALL + " Tak będą wyglądać informacje")
    print(Fore.YELLOW + "[LAUNCH]" + Style.RESET_ALL + " Tak ostrzeżenia")
    print(Fore.RED + "[LAUNCH]" + Style.RESET_ALL + " A tak błędy")
    print(Fore.GREEN + "[LAUNCH]" + Style.RESET_ALL + " Uruchamianie " + Fore.YELLOW + "main.py")
    print(" ")

    os.system(F'python {script_dir}/app/main.py 2>/dev/null')

# Update
else:
    os.system('git pull')
    os.system(F'setsid python {script_dir}/launch.py launch >/dev/null 2>&1 < /dev/null &')