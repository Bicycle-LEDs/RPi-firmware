# Import libs
import sys, random, string, os, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[TTS] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[TTS] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

def tts(language, message):
    try: 
        # Try importing text-to-speech
        from gtts import gTTS

        # Generate random string for filename - to prevent multi-script-running issues
        digits = random.choices(string.digits, k=3)
        letters = random.choices(string.ascii_letters, k=6)
        filename = script_dir + '/' + ''.join(random.sample(digits + letters, 9)) + '.mp3'

        # Generate audio file in argument 1 language and saying argument 2 text 
        TTS = gTTS(message, lang=language, lang_check=False)
        TTS.save(filename)
        # Read audio file
        os.system('mpg123 ' + filename)
        os.remove(filename)
        return True
    
    # Ctrl + C clicked
    except KeyboardInterrupt:
        print(ctrlCMsg)
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