# Import libraries
import os, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[BINGCHAT] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[BINGCHAT] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

try:
    # Import chatgpt library
    from EdgeGPT import Chatbot, ConversationStyle

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
            # Authorize to bing ai
            print(infoMsg + "Logowanie do bingchat...")
            bot = Chatbot(cookies=login["bingchat"]["cookies"])

            # Generate response
        async def generate():
            bot = Chatbot(cookies=login["bingchat"]["cookies"])
            # Generate response
            print(infoMsg + "(TTS) Łączenie z bing chat i generowanie odpowiedzi...")
            os.system(F'python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź"')
            message = await bot.ask(prompt=text + " - ogranicz odpowiedź do 30 słów", conversation_style=ConversationStyle.precise)
            return message


            print(infoMsg + "(TTS) Łączenie z bing chat i generowanie odpowiedzi...")
            os.system(F'python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź"')
            message = bot.ask(prompt=text + " - ogranicz odpowiedź do 30 słów", conversation_style=ConversationStyle.balanced)
            print(infoMsg + "(TTS) Odpowiedź: " + colorama.Fore.CYAN + message)
            if tts('pl', message) == 3:
                print(ctrlCMsg)

        except:
            # Problem connecting / generating response
            print(errorMsg + "(TTS) Połączenie z czatbotem nieudane")
            if tts('pl', "Połączenie nieudane") == 3:
                print(ctrlCMsg)


# Ctrl + C handle
except KeyboardInterrupt:
    print(ctrlCMsg)

# Critical error
except:
    print(errorMsg + "Wystąpił nieprzewidziany błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')