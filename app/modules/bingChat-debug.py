# Import libraries
import os, json, colorama, asyncio
from collections import namedtuple
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Which phrases to delete from response (it's based on web, so sometimes calls return some strange things)
toDelete=[
    "Czy chcesz wiedzieć coś więcej na ten temat?"
    "[^1^]", "[^2^]", "[^3^]", "[^4^]", "[^5^]", "[^6^]"
]

# Default message starts
infoMsg = colorama.Fore.GREEN + "[BINGCHAT] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[BINGCHAT] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

# Import chatgpt library
from EdgeGPT import Chatbot, ConversationStyle

# Import speechrecognition and tts scripts
from helpers.speechRecognition import speechRecognition
from helpers.textToSpeech import tts

# Play sound
os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
print(infoMsg + "Uruchamianie rozpoznawania mowy...")

# Recognize voice
text = "czy kebab jest dobry"

# If unknown value or module error play error sound
if text == 1 or text == 2 or text == False:
    os.system(F'setsid mpg123 {script_dir}/sounds/connectionError.mp3 >/dev/null')

# If speech recognized     
else:

    # Open credentials file
    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

        # Authorize to bing ai
        print(infoMsg + "Logowanie do bingchat...")
        async def generate():
            bot = Chatbot(cookies=login["bingchat"]["cookies"])
            # Generate response
            print(infoMsg + "(TTS) Łączenie z bing chat i generowanie odpowiedzi...")
            os.system(F'python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź"')
            message = await bot.ask(prompt=text + " - ogranicz odpowiedź do 30 słów", conversation_style=ConversationStyle.precise)
            return message
        

        message = asyncio.run(generate())["item"]["messages"][1]["text"].replace("substring", "")
        message
        print(infoMsg + "(TTS) Odpowiedź: " + colorama.Fore.CYAN)
        print(message)
        if tts('pl', message) == 3:
            print(ctrlCMsg)