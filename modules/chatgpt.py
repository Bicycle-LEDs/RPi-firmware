import os, json
try:
    import speech_recognition as sr
    from gtts import gTTS
    import openai
    script_dir=os.path.dirname(os.path.realpath(__file__))

    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

    openai.api_key = login["openai"]["apiKey"]

    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        print("[INFO] Listening...")

    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        tts = gTTS("Czekam na odpowiedź od chatgpt", lang='pl', lang_check=False)
        tts.save('waiting.mp3')
        os.system('setsid mpg123 waiting.mp3 >/dev/null 2>&1 < /dev/null &')
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
        message = "Odpowiedź: " + completion.choices[0].message.content
        print("[RESULT] Odpowiedź: " + message)

    except sr.UnknownValueError:
        print("[ERR] Audio nierozpoznawalne")
        message = "Wystąpił problem z rozpoznaniem mowy"

    except sr.RequestError as e:
        print("[ERR] Problem z google speech engine; {0}".format(e))
        message = "Wystąpił problem z połączeniem"

    tts = gTTS(message, lang='pl', lang_check=False)
    tts.save('response.mp3')
    os.system('mpg123 response.mp3')
    os.remove('response.mp3')
    os.remove('waiting.mp3')
    print("[INFO] Wykonano skrypt.")

except:
    print("[ERR] Wykonywanie skryptu chatgpt.py nieudane.")
    from gtts import gTTS
    tts = gTTS("Wystąpił krytyczny błąd w programie chatgpt", lang='pl', lang_check=False)
    tts.save('response.mp3')
    os.system('mpg123 response.mp3')
    os.remove('response.mp3')