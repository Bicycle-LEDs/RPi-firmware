from pydexcom import Dexcom
from gtts import gTTS
import os, json

with open('../credentials.json') as f:
    login = json.load(f)

tts = gTTS("Łączenie...", lang='pl', lang_check=False)
tts.save('workingOnIt.mp3')
os.system('mpg123 workingOnIt.mp3')
os.remove('workingOnIt.mp3')

# Login
try:
    dexcom = Dexcom(login["dexcom"]["login"], login["dexcom"]["password"], ous=login["dexcom"]["OutsideUS"])
    bg = dexcom.get_current_glucose_reading()

    # Get reading
    print("Glucose level: ")
    print(bg.value)

    # Create nice trend transcription
    if bg.trend == 1:
        trend = "bardzo szybko rośnie"
    elif bg.trend == 2:
        trend = "szybko rośnie"
    elif bg.trend == 3:
        trend = "powoli wzrasta"
    elif bg.trend == 4:
        trend = "jest stabilny"
    elif bg.trend == 5:
        trend = "lekko spada"
    elif bg.trend == 6:
        trend = "sporawo spada"
    elif bg.trend == 7:
        trend = "mocno spada"
    else:
        trend = "są problemy z wyznaczeniem trendu"

    # Read loudly
    tts = gTTS("Twój cukier to " + str(bg.value) + " i " + trend, lang='pl', lang_check=False)

except:
    tts = gTTS("Połączenie nieudane", lang='pl', lang_check=False)

tts.save('dexcom-value.mp3')
os.system('mpg123 dexcom-value.mp3')
os.remove('dexcom-value.mp3')