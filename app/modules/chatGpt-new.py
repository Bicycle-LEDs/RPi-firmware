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
    from helpers.speechRecognition import speechRecognition
    from helpers.textToSpeech import tts

    # Play sound
    os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
    print(infoMsg + "Uruchamianie rozpoznawania mowy...")

    # Recognize voice
    text = speechRecognition('pl-PL')

     # If unknown value or module error play error sound
    if text == 1 or text == 2 or text == False:
        os.system(F'setsid mpg123 {script_dir}/sounds/connectionError.mp3 >/dev/null')

    # If speech recognized     
    else:

        # Open credentials file
        with open(script_dir + '/../credentials.json') as f:
            login = json.load(f)

        try:
            # Authorize to openai chatgpt
            print(infoMsg + "Logowanie do openai...")
            openai.api_key = login["openai"]["apiKey"]

            # Generate response
            print(infoMsg + "(TTS) Łączenie z chatgpt i generowanie odpowiedzi...")
            os.system(F'python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź"')

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text + " - ogranicz odpowiedź do 30 słów"}], max_tokens=100)
            message = completion.choices[0].message.content
            print(infoMsg +  "(TTS) Odpowiedź: " + colorama.Fore.CYAN + message)
            tts('pl', message)

        except:
            print(errorMsg + "(TTS) Połączenie z czatbotem nieudane")
            tts('pl', "Połączenie nieudane")


except:
    print(errorMsg + "Wystąpił nieprzewidziany błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')