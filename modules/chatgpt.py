import os, json
script_dir=os.path.dirname(os.path.realpath(__file__))

try:
    import speech_recognition as sr
    from gtts import gTTS
    import openai

    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

    openai.api_key = login["openai"]["apiKey"]

    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
        audio = r.listen(source)
        print("[INFO] Rozpoznawanie...")

    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        tts = gTTS("Zaczekaj na odpowiedź", lang='pl', lang_check=False)
        tts.save('waiting.mp3')
        os.system('setsid mpg123 waiting.mp3 >/dev/null 2>&1 < /dev/null &')
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text + " - odpowiedz w maksymalnie 20 słowach"}], max_tokens=100)
        message = completion.choices[0].message.content
        print("[RESULT] " + message)

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
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')
