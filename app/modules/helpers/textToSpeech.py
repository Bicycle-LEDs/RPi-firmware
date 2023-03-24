# Import system packages
import sys, random, string, os

def tts(language, message):
    try: 
        # Try importing text-to-speech
        from gtts import gTTS

        # Generate random string for filename - to prevent multi-script-running issues
        digits = random.choices(string.digits, k=3)
        letters = random.choices(string.ascii_letters, k=6)
        filename = random.sample(digits + letters, 9) + '.mp3'

        # Generate audio file in argument 1 language and saying argument 2 text 
        tts = gTTS(message, lang=language, lang_check=False)
        tts.save('../temp/' + filename)
        
        # Read audio file
        os.system('mpg123 ../temp/' + filename)
        os.remove('../temp/' + filename)
        return True
    
    except:
        # Return error
        return False

# Run function if called as file
try: 
    tts(sys.argv[1], sys.argv[2])
except:
    print()