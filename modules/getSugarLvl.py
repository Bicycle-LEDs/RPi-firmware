from pydexcom import Dexcom
from gtts import gTTS
import os, json
script_dir=os.path.dirname(os.path.realpath(__file__))

with open(script_dir + '/../credentials.json') as f:
    login = json.load(f)

print("[INFO] Connecting to Dexcom...")
tts = gTTS("Łączenie z Dexcom...", lang='pl', lang_check=False)
tts.save('workingOnIt.mp3')
os.system('setsid mpg123 workingOnIt.mp3 && rm -rf workingOnIt.mp3 >/dev/null 2>&1 < /dev/null &')

# Login
try:
    dexcom = Dexcom(login["dexcom"]["login"], login["dexcom"]["password"], ous=login["dexcom"]["OutsideUS"])
    bg = dexcom.get_current_glucose_reading()

    # Get reading
    print("[RESULT] Glucose level: " + str(bg.value) + " - " + bg.trend_description + "(" + bg.trend_arrow + ")")

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
    tts = gTTS(str(bg.value) + " i " + trend, lang='pl', lang_check=False)

except:
    tts = gTTS("Połączenie nieudane", lang='pl', lang_check=False)

tts.save('dexcom-value.mp3')
os.system('mpg123 dexcom-value.mp3')
os.remove('dexcom-value.mp3')
print("[INFO] Completed.")