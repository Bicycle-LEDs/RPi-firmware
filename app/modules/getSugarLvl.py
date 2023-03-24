import os, json, colorama, sys
colorama.init()
script_dir=os.path.dirname(os.path.realpath(__file__))
infoMsg = colorama.Fore.GREEN + "[INFO]" + colorama.Style.RESET_ALL + " "
errorMsg = colorama.Fore.RED + "[ERROR]" + colorama.Style.RESET_ALL + " "

# Import tts script
sys.path.append('../base')
from textToSpeech import tts

try:
    from pydexcom import Dexcom

    # Read credentials file
    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

    # Play sound
    os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
    
    print(infoMsg + "Łączenie z serwerem...")
    # Text to speech but async
    os.system(F'python {script_dir}/../base/textToSpeech.py pl "Łączenie z dexcom"')    

    # Login
    try:
        dexcom = Dexcom(login["dexcom"]["login"], login["dexcom"]["password"], ous=login["dexcom"]["OutsideUS"])
        bg = dexcom.get_current_glucose_reading()

        # Get reading
        print(infoMsg + "Poziom glukozy: " + colorama.Fore.CYAN+str(bg.value) + colorama.Style.RESET_ALL+" - " + colorama.Fore.CYAN+bg.trend_description + " " + bg.trend_arrow)

        # Create nice trend transcription
        if bg.trend == 1:
            trend = "bardzo szybko rośnie"
        elif bg.trend == 2:
            trend = "szybko rośnie"
        elif bg.trend == 3:
            trend = "powoli wzrasta"
        elif bg.trend == 4:
            trend = "stabilnie"
        elif bg.trend == 5:
            trend = "lekko spada"
        elif bg.trend == 6:
            trend = "sporawo spada"
        elif bg.trend == 7:
            trend = "mocno spada"
        else:
            trend = "wyznaczenie trendu nie powiodło się"

        # Read loudly
        tts('pl', bg.value + " i " + trend)

    except:
        tts('pl', "Połączenie nieudane")

except:
    print(errorMsg + "Wystąpił błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')