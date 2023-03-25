# Import libraries
import os, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[REC] " + colorama.Style.RESET_ALL
startingSpace = " "*len("[REC] ")
warningMsg = colorama.Fore.YELLOW + "[REC] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[REC] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

def speechRecognition(lang, startSound=False):
    try: 
        # Try importing speechRecognition
        import speech_recognition as sr
        r = sr.Recognizer()

        # Listen
        with sr.Microphone() as source:            
            print(infoMsg + "Słuchanie...")
            if startSound:
                os.system(F'setsid mpg123 {script_dir}/../../sounds/gotIt.mp3 >/dev/null')

            audio = r.listen(source)

        # Get Google opinion on what was said
        print(startingSpace + "Próba przetworzenia na tekst...")
        try:
            text = r.recognize_google(audio, language=lang).lower()
            print(startingSpace + F"Rozpoznany tekst: {colorama.Fore.CYAN}{text}")
            return text

        # Unknown speech
        except sr.UnknownValueError:
            print(warningMsg + "Tekst nierozpoznany")
            return 2

        # Google error
        except sr.RequestError as e:
            print(errorMsg + "Problem z google speech engine: " + e)
            return 1
    
    # Ctrl + C clicked
    except KeyboardInterrupt:
        print(ctrlCMsg)
        return 3

    # Critical error
    except:
        print(errorMsg + "Wystąpił nieprzewidziany błąd w skrypcie")
        return False