from pydexcom import Dexcom
from gtts import gTTS
import os

tts = gTTS("Łączenie...", lang='pl')
tts.save('workingOnIt.mp3')
os.system('mpg123 workingOnIt.mp3')
os.remove('workingOnIt.mp3')

# Login
try:
    dexcom = Dexcom("USERNAME", "PASSWORD", ous=True)
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
    tts = gTTS("Twój cukier to " + str(bg.value) + " i " + trend, lang='pl')

except:
    tts = gTTS("Połączenie nieudane", lang='pl')

tts.save('dexcom-value.mp3')
os.system('mpg123 dexcom-value.mp3')
os.remove('dexcom-value.mp3')