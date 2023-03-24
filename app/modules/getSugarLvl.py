# Import libs
import os, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[GETSUGARLVL] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[GETSUGARLVL] " + colorama.Style.RESET_ALL

try:
    # Import dexcom library
    from pydexcom import Dexcom
    # Import tts script
    from helpers.textToSpeech import tts

    # Read credentials file
    with open(script_dir + '/../credentials.json') as f:
        login = json.load(f)

    # Play sound
    os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null')
    print(infoMsg + "(TTS) Łączenie z serwerem...")
    os.system(F'python {script_dir}/helpers/textToSpeech.py pl "Łączenie z dexcom"')    

    try:
        # Try logging-in
        dexcom = Dexcom(login["dexcom"]["login"], login["dexcom"]["password"], ous=login["dexcom"]["OutsideUS"])

        # Get reading
        bg = dexcom.get_current_glucose_reading()

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

        # Read and print
        print(infoMsg + "(TTS) Poziom cukru: " + colorama.Fore.CYAN+str(bg.value) + colorama.Style.RESET_ALL+" - " + colorama.Fore.CYAN+trend + " " + bg.trend_arrow)
        tts('pl', str(bg.value) + " i " + trend)

    # Login error
    except:
        print(errorMsg + "(TTS) Połączenie z Dexcom nieudane")
        tts('pl', "Połączenie nieudane")

# Critical error handling
except:
    print(errorMsg + "Wystąpił nieprzewidziany błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')