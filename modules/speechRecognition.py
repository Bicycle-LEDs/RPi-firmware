import speech_recognition as sr
import os, json

with open('./modules.json') as f:
    modules = json.load(f)

# do some more unrelated things
while True: 
    
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        print("Listening!")

        # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        for module in modules:
                for alias in module["aliases"]:
                    index = text.find(alias)
                    if index != -1:
                        os.system(F'setsid mpg123 gotIt.mp3 >/dev/null 2>&1 < /dev/null &')
                        os.system(module["exec"])
            
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))