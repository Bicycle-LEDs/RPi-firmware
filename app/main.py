# Import system libs
import os, sys, json, time, colorama
colorama.init()    

# Import speechrecognition script 
from modules.helpers.speechRecognition import speechRecognition

# Default message starts
infoMsg = colorama.Fore.GREEN + "[MAIN] " + colorama.Style.RESET_ALL
warningMsg = colorama.Fore.YELLOW + "[MAIN] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[MAIN] " + colorama.Style.RESET_ALL

# Import modules.json
script_dir=os.path.dirname(os.path.realpath(__file__))
with open(script_dir + '/modules/modules.json') as f:
    modules = json.load(f)

# Var to count errors and play appropriate sounds
countErrors=0

def ctrlCProcedure():
    print(errorMsg + "Użyto Ctrl + C, kończę działanie programu.")
    sys.exit(0)

def load_module(module):
    # module_path = "mypackage.%s" % module
    module_path = module
    if module_path in sys.modules:
        return sys.modules[module_path]
    return __import__(module_path, fromlist=[module])

print(infoMsg + "Serwer rozpoznawania mowy aktywny - użyj" + colorama.Fore.RED + " Ctrl + C " + colorama.Style.RESET_ALL + ", aby wyjść")
# Loop forever
while True:

    try:
        # Recognize speech
        text = speechRecognition('pl-PL')


        # If critical error
        if text == 1:
            # Error counter +1
            countErrors+=1
            # If not third error
            if countErrors!=3:
                os.system(F'setsid mpg123 {script_dir}/sounds/connectionError.mp3 >/dev/null')
            else:
                os.system(F'setsid mpg123 {script_dir}/sounds/connectionErrorLong.mp3 >/dev/null')
        
        # If unknown value
        elif text == 2:
            # Reset connection error counter
            countErrors=0
        
        # If critical module error
        elif text == False:
            time.sleep(3)

        # If Ctrl + C used
        elif text == 3: 
            ctrlCProcedure()

        # If speech recognized     
        else:
            countErrors=0
            # For every module
            for module in modules:
                # For every alias
                for alias in module["aliases"]:
                    index = text.find(alias)
                    # If alias found
                    if index != -1:
                        # If needed to be executed in background
                        if module["execInBackground"]:

                            # Outdated module message
                            if module["outdated"]:
                                message=warningMsg + "Przestarzały skrypt " + colorama.Fore.YELLOW + module["exec"] + colorama.Style.RESET_ALL + " został uruchomiony w tle"
                            # Normal message
                            else:
                                message=infoMsg + "Skrypt " + colorama.Fore.YELLOW + module["exec"] + colorama.Style.RESET_ALL + " został uruchomiony w tle"
                            print(message)
                            # Execute
                            os.system(F'setsid python {script_dir}/modules/{module["exec"]} >/dev/null 2>&1 < /dev/null &')
                        
                        # If executed on top
                        else:
                            print()
                            # Outdated module message
                            if module["outdated"]:
                                message=warningMsg + "Uruchamianie przestarzałego skryptu " + colorama.Fore.YELLOW + module["exec"]
                            # Normal message
                            else:
                                message=infoMsg + "Uruchamianie " + colorama.Fore.YELLOW + module["exec"]
                            print(message)
                            # Execute
                            main = load_module(F'{script_dir}/modules/{module["exec"]}')
                            check = main.main()
                            if check == 3:
                                ctrlCProcedure()
                            print(infoMsg + "Moduł zakończył działanie")
                            print()    

    except KeyboardInterrupt:
        ctrlCProcedure()