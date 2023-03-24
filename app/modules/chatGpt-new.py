# Import libraries
import os, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[CHATGPT] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[CHATGPT] " + colorama.Style.RESET_ALL

try:
    # Import chatgpt library
    import openai

    # Import speechrecognition and tts scripts
    text = speechRecognition('pl-PL')

    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

    openai.api_key = login["openai"]["apiKey"]

    r = sr.Recognizer()
    with sr.Microphone() as source:
        os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
        print(infoMsg + "Słuchanie zapytania...")
        audio = r.listen(source)
        print(infoMsg + "Przerabianie na tekst...")

    try:
        text = r.recognize_google(audio, language='pl-PL').lower()
        print(infoMsg + "Zapytanie: " + colorama.Fore.CYAN + text)
        print(infoMsg + "Generowanie odpowiedzi...")
        tts = gTTS("Zaczekaj na odpowiedź", lang='pl', lang_check=False)
        tts.save('waiting.mp3')
        os.system('setsid mpg123 waiting.mp3 >/dev/null 2>&1 < /dev/null &')
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text + " - ogranicz odpowiedź do 30 słów"}], max_tokens=100)
        message = completion.choices[0].message.content
        print(infoMsg +  "Odpowiedź: " + colorama.Fore.CYAN + message)

    except sr.UnknownValueError:
        print(errorMsg +  "Przerobienie audio na tekst nieudane")
        message = "Wystąpił problem z rozpoznaniem mowy"

    except sr.RequestError as e:
        print(errorMsg + "Problem z google speech engine: " + colorama.Fore.CYAN + e)
        message = "Wystąpił problem z połączeniem"

    tts = gTTS(message, lang='pl', lang_check=False)
    tts.save('response.mp3')
    os.system('mpg123 response.mp3')
    os.remove('response.mp3')
    os.remove('waiting.mp3')

except:
    print(errorMsg + "Wystąpił błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')