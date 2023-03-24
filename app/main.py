import speech_recognition as sr
import os, json
import colorama
colorama.init()

infoMsg = colorama.Fore.GREEN + "[MAIN] " + colorama.Style.RESET_ALL
warningMsg = colorama.Fore.YELLOW + "[MAIN] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[MAIN] " + colorama.Style.RESET_ALL

script_dir=os.path.dirname(os.path.realpath(__file__))
with open(script_dir + '/modules/modules.json') as f:
    modules = json.load(f)

i=0

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(infoMsg + "Słuchanie...")
        audio = r.listen(source)
        print(infoMsg + "Próba przetworzenia na tekst...")

        # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        print(infoMsg + "Rozpoznany tekst: " + colorama.Fore.CYAN + text)
        i=0
        for module in modules:
                for alias in module["aliases"]:
                    index = text.find(alias)
                    if index != -1:
                        if module["execInBackground"]:
                            if module["outdated"]:
                                message=infoMsg + "Przestarzały skrypt " + colorama.Fore.YELLOW + module["exec"] + colorama.Style.RESET_ALL + " został uruchomiony w tle"
                            else:
                                message=infoMsg + "Skrypt " + colorama.Fore.YELLOW + module["exec"] + colorama.Style.RESET_ALL + " został uruchomiony w tle"
                            print(message)
                            os.system(F'setsid python {script_dir}/modules/{module["exec"]} >/dev/null 2>&1 < /dev/null &')
                        else:
                            print(" ")
                            if module["outdated"]:
                                message=infoMsg + "Uruchamianie przestarzałego modułu " + colorama.Fore.YELLOW + module["exec"]
                            else:
                                message=infoMsg + "Uruchamianie " + colorama.Fore.YELLOW + module["exec"]
                            print(message)
                            os.system(F'python {script_dir}/modules/{module["exec"]}')
                            print(" ")
            
    except sr.UnknownValueError:
        i=0
        print(warningMsg + "Tekst nierozpoznany")
    except sr.RequestError as e:
        i+=1
        print(errorMsg + "Problem z google speech engine: " + colorama.Fore.CYAN + e)
        if i!=3:
            os.system(F'setsid mpg123 {script_dir}/sounds/connectionError.mp3 >/dev/null')
        else:
            os.system(F'setsid mpg123 {script_dir}/sounds/connectionErrorLong.mp3 >/dev/null')
