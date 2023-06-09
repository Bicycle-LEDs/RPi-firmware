# Import libraries
import os, sys, json, colorama, asyncio
colorama.init()

# Argument parsed will be AI type (openai, bing), if no argument fallback to bing
try:
    chatType = sys.argv[1].lower()
except:
    chatType = 'bing'

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Phrases to delete from response (it's based on web, so sometimes calls return some strange things)
bingToDelete = [
    "Czy chcesz wiedzieć coś więcej na ten temat?",
    "Czy chcesz wiedzieć więcej?",
    "Czy chcesz wiedzieć coś więcej?"
    "[^1^]", "[^2^]", "[^3^]", "[^4^]", "[^5^]", "[^6^]",
]

# Default message starts
if chatType=='openai': textForCons='AI-CGPT'
else: 
    chatType=='bing'
    textForCons='AI-BING'
infoMsg = colorama.Fore.GREEN + F"[{textForCons}] " + colorama.Style.RESET_ALL
startingSpace = " "*len(F"[{textForCons}] ")
warningMsg = colorama.Fore.YELLOW + F"[{textForCons}] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + F"[{textForCons}] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

try:
    # Import speechrecognition and tts scripts
    from helpers.speechRecognition import speechRecognition
    from helpers.textToSpeech import tts
    
    # Recognize voice
    print(infoMsg + "Uruchamianie rozpoznawania mowy...")
    text = speechRecognition(lang='pl-PL', startSound=True)

    if text == 1 or text == 2 or text == False:
        print(warningMsg + "(TTS) Mowa nierozpoznana")
        if tts('pl', "Mowa nierozpoznana") == 3: print(ctrlCMsg)
        chatType=0
    elif text == 3:
        print(ctrlCMsg)
        chatType=0

    # Open credentials file
    with open(script_dir + '/../settings.json') as f:
        login = json.load(f)["chatAI"]

    try:

        # If using openai
        if chatType=="openai":     
            import openai

            # Authorize to openai chatgpt
            print(infoMsg + "Logowanie do openai...")
            openai.api_key = login["openai"]["apiKey"]

            # Generate response
            print(startingSpace + "(TTS) Łączenie z chatgpt i generowanie odpowiedzi...")
            os.system(F'setsid python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź" >/dev/null 2>&1 < /dev/null &')
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text + " - ogranicz odpowiedź do 30 słów"}], max_tokens=100)
            message = completion.choices[0].message.content


        elif chatType=="bing":
            import EdgeGPT

            # Authorize to bing AI
            print(infoMsg + "Logowanie do bingchat...")
            bot = EdgeGPT.Chatbot(cookies=login["bing"]["cookies"])

            # Generate response
            async def generate():
                print(startingSpace + "(TTS) Łączenie z bing chat i generowanie odpowiedzi...")
                os.system(F'setsid python {script_dir}/helpers/textToSpeech.py pl "Zaczekaj na odpowiedź" >/dev/null 2>&1 < /dev/null &')
                msg = await bot.ask(prompt=text + " - ogranicz odpowiedź do 30 słów", conversation_style=EdgeGPT.ConversationStyle.precise)
                return msg
    
            message = asyncio.run(generate())["item"]["messages"][1]["text"]

            # Delete some garbage from answer 
            for rm in bingToDelete: message = message.replace(rm, "")

        if not chatType==0:            
            # Output message
            print(startingSpace + F"(TTS) Odpowiedź: {colorama.Fore.CYAN}{message}")
            if tts('pl', message) == 3: print(ctrlCMsg)

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