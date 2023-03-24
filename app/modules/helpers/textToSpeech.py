# Import libs
import sys, random, string, os, colorama
colorama.init()

# Default message starts
errorMsg = colorama.Fore.RED + "[TEXTTOSPEECH] " + colorama.Style.RESET_ALL

def tts(language, message):
    try: 
        # Try importing text-to-speech
        from gtts import gTTS

        # Generate random string for filename - to prevent multi-script-running issues
        digits = random.choices(string.digits, k=3)
        letters = random.choices(string.ascii_letters, k=6)
        filename = ''.join(random.sample(digits + letters, 9)) + '.mp3'

        # Generate audio file in argument 1 language and saying argument 2 text 
        TTS = gTTS(message, lang=language, lang_check=False)
        TTS.save(filename)
        # Read audio file
        os.system('mpg123 ' + filename)
        os.remove(filename)
        return True
    
    # Ctrl + C clicked
    except KeyboardInterrupt:
        print("\n" + errorMsg + "Użyto Ctrl + C, poinformowano nadrzędny skrypt")
        return 3
    
    except:
        # Return error
        print(errorMsg + "Wystąpił błąd w skrypcie")
        return False

# Run function if called as file
try:
    tts(sys.argv[1], sys.argv[2])
except:
    pass