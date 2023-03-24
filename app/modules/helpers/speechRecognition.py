# Import libraries
import colorama
colorama.init()

# Default message starts
infoMsg = colorama.Fore.GREEN + "[SPEECHRECOGNITION] " + colorama.Style.RESET_ALL
warningMsg = colorama.Fore.YELLOW + "[SPEECHRECOGNITION] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[SPEECHRECOGNITION] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

def speechRecognition(lang):
    try: 
        # Try importing speechRecognition
        import speech_recognition as sr
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print(infoMsg + "Słuchanie...")
            audio = r.listen(source)

        # Get Google opinion on what was said
        print(infoMsg + "Próba przetworzenia na tekst...")
        try:
            text = r.recognize_google(audio, language=lang).lower()
            print(infoMsg + "Rozpoznany tekst: " + colorama.Fore.CYAN + text)
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