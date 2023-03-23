import speech_recognition as sr
import os, json
import colorama
colorama.init()

script_dir=os.path.dirname(os.path.realpath(__file__))
with open(script_dir + '/modules.json') as f:
    modules = json.load(f)

i=0

print(colorama.Fore.BLUE + "Listening!" + colorama.Style.RESET_ALL)
while True:
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        print(colorama.Fore.GREEN + "You're talking, trying to recognize..." + colorama.Fore.CYAN)

        # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        i=0
        for module in modules:
                for alias in module["aliases"]:
                    index = text.find(alias)
                    if index != -1:
                        os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
                        os.system(F'setsid python {script_dir}/{module["exec"]} >/dev/null 2>&1 < /dev/null &')
            
    except sr.UnknownValueError:
        i=0
        print("Audio nierozpoznawalne")
    except sr.RequestError as e:
        i+=1
        print("Problem z google speech engine, brak internetu albo coś; {0}".format(e))
        if(i!=3):
            os.system(F'setsid mpg123 {script_dir}/../sounds/connectionError.mp3 >/dev/null')
        else:
            os.system(F'setsid mpg123 {script_dir}/../sounds/connectionErrorLong.mp3 >/dev/null')
