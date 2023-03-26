# Import system libs
import os, sys, json, time, colorama
colorama.init()    

# Import scripts
from modules.helpers.speechRecognition import speechRecognition
from modules.helpers.OLEDRefresh import OLEDRefresh

# Default message starts
infoMsg = colorama.Fore.GREEN + "[MAIN] " + colorama.Style.RESET_ALL
warningMsg = colorama.Fore.YELLOW + "[MAIN] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[MAIN] " + colorama.Style.RESET_ALL
breakMsg = "------------------------" + colorama.Style.RESET_ALL

# Import modules.json
script_dir=os.path.dirname(os.path.realpath(__file__))
with open(script_dir + '/modules/modules.json') as f:
    modules = json.load(f)

# Var to count errors and play appropriate sounds
countErrors=0

# CtrlC script
def ctrlCProcedure():
    print(infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", kończę działanie programu.")
    sys.exit(0)


print(infoMsg + "Serwer rozpoznawania mowy aktywny - użyj" + colorama.Fore.RED + " Ctrl + C " + colorama.Style.RESET_ALL + "(kilka razy), aby wyjść")

# Check if OLED accessible
if OLEDRefresh(): UseOLED=True
else: UseOLED=False

# Loop forever
while True:

    try:
        # Recognize speech
        if UseOLED: OLEDRefresh()
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
                            print(F"{infoMsg}Skrypt {colorama.Fore.YELLOW}{module['exec']}{colorama.Style.RESET_ALL} został uruchomiony w tle")
                            # Execute
                            os.system(F'setsid python {script_dir}/modules/{module["exec"]} >/dev/null 2>&1 < /dev/null &')
                        
                        # If executed on top
                        else:
                            print()
                            print(F"{infoMsg}Uruchamianie {colorama.Fore.YELLOW}{module['exec']}")
                            if UseOLED: OLEDRefresh(module["exec"])
                            print(breakMsg)
                            # Execute
                            os.system(F'python {script_dir}/modules/{module["exec"]}')
                            if UseOLED: OLEDRefresh()
                            print(colorama.Fore.BLUE + breakMsg)
                            print()

    except KeyboardInterrupt:
        ctrlCProcedure()