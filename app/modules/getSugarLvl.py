# Import libs
import os, sys, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[DEXC] " + colorama.Style.RESET_ALL
startingSpace = " "*len("[DEXC] ")
errorMsg = colorama.Fore.RED + "[DEXC] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

try:
    # Import dexcom library
    from pydexcom import Dexcom
    # Import tts script
    from helpers.textToSpeech import tts

    # Read credentials file
    with open(script_dir + '/../settings.json') as f:
        authorize = json.load(f)["dexcom"]

    # Play sound
    os.system(F'setsid mpg123 {script_dir}/../sounds/gotIt.mp3 >/dev/null 2>&1 < /dev/null &')
    print(infoMsg + "(TTS) Łączenie z serwerem...")
    os.system(F'setsid python {script_dir}/helpers/textToSpeech.py pl "Łączenie z dexcom" >/dev/null 2>&1 < /dev/null &')    

    try:
        # Try logging-in
        dexcom = Dexcom(authorize["login"], authorize["password"], ous=authorize["OutsideUS"])

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
        print(startingSpace + F"(TTS) Poziom cukru: {colorama.Fore.CYAN}{str(bg.value)}{colorama.Style.RESET_ALL} - {colorama.Fore.CYAN}{trend} {bg.trend_arrow}")
        if tts('pl', str(bg.value) + " i " + trend) == 3:
            print(ctrlCMsg)

    # Login error
    except:
        print(errorMsg + "(TTS) Połączenie z Dexcom nieudane")
        if tts('pl', "Połączenie nieudane") == 3: print(ctrlCMsg)

# Ctrl + C handling
except KeyboardInterrupt:
    print(ctrlCMsg)

# Critical error handling
except:
    print(errorMsg + "Wystąpił nieprzewidziany błąd w skrypcie")
    os.system(F'mpg123 {script_dir}/../sounds/scriptError.mp3')