import speech_recognition as sr
import os, json
import colorama
colorama.init()

script_dir=os.path.dirname(os.path.realpath(__file__))
with open(script_dir + '/modules.json') as f:
    modules = json.load(f)

i=0

while True:
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        print(colorama.Fore.GREEN + "[INFO] Słuchanie!")
        audio = r.listen(source)
        print(colorama.Fore.CYAN + "[INFO] Próba rozpoznania..." + colorama.Fore.YELLOW)

        # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        i=0
        for module in modules:
                for alias in module["aliases"]:
                    index = text.find(alias)
                    if index != -1:
                        print(colorama.Fore.GREEN + "[INFO] Uruchamianie " + module["exec"] + colorama.Fore.CYAN)
                        if module["execInBackground"]:
                            os.system(F'setsid python {script_dir}/{module["exec"]} >/dev/null 2>&1 < /dev/null &')
                        else:
                            os.system(F'python {script_dir}/{module["exec"]}')
            
    except sr.UnknownValueError:
        i=0
        print(colorama.Fore.YELLOW + "[WARNING] Audio nierozpoznawalne")
    except sr.RequestError as e:
        i+=1
        print(colorama.Fore.RED + "[ERR] Problem z google speech engine; {0}".format(e))
        if i!=3:
            os.system(F'setsid mpg123 {script_dir}/../sounds/connectionError.mp3 >/dev/null')
        else:
            os.system(F'setsid mpg123 {script_dir}/../sounds/connectionErrorLong.mp3 >/dev/null')
