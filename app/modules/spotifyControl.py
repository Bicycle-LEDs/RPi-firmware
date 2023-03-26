# Import libs
import os, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[SPOT] " + colorama.Style.RESET_ALL
startingSpace = " "*len("[SPOT] ")
warningMsg = colorama.Fore.YELLOW + "[SPOT] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[SPOT] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"

try:
    # Import scripts
    import spotipy
    from helpers.speechRecognition import speechRecognition
    from helpers.textToSpeech import tts

    # Recognize voice
    print(infoMsg + "Uruchamianie rozpoznawania mowy...")
    #text = speechRecognition(lang='pl-PL', startSound=True)
    text="zatrzymaj"

    if text == 1 or text == 2 or text == False:
        print(warningMsg + "(TTS) Mowa nierozpoznana")
        if tts('pl', "Mowa nierozpoznana") == 3: print(ctrlCMsg)
    elif text == 3:
        print(ctrlCMsg)
    else:

        # Read credentials file
        with open(script_dir + '/../settings.json') as f:
            authorize = json.load(f)["spotify"]
        
        # Get available commands
        with open(script_dir + '/modules.json') as f:
            modules = json.load(f)
            for module in modules:
                if module["name"] == 'Spotify': availableCommands = module["commands"]

        command = 0
        for cmd in availableCommands["next"]:
            index = text.find(cmd)
            if index != -1:
                command = "następny"
                text = text.replace(cmd, "")
        
        for cmd in availableCommands["previous"]:
            index = text.find(cmd)
            if index != -1:
                command = "poprzedni"
                text = text.replace(cmd, "")

        for cmd in availableCommands["play/pause"]:
            index = text.find(cmd)
            if index != -1:
                command = "odtwórz/wstrzymaj"
                text = text.replace(cmd, "")  

        for cmd in availableCommands["search"]:
            index = text.find(cmd)
            if index != -1:
                command = "wyszukaj"
                text = text.replace(cmd, "")  
        
        if command:
            print(infoMsg + F"(TTS) Łączenie z serwerem (polecenie: {command})...")
            os.system(F'setsid python {script_dir}/helpers/textToSpeech.py pl "Łączenie ze spotify" >/dev/null 2>&1 < /dev/null &')    

            # Login to spotify
            spotify = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=authorize['clientID'],
                                                                          client_secret=authorize['clientSecret'],
                                                                          redirect_uri="http://localhost:8080/callback/"))
            # Play/pause
            if command == "odtwórz/wstrzymaj":
                print(spotify.current_playback())
                print('hmm')

                if spotify.current_playback():
                    message = 'Zatrzymano utwór'

                else:
                    message = 'Wznowiono odtwarzanie'

            # Next
            elif command == "następny":
                spotify.next_track()
                message = 'Pominięto utwór'

            # Previous
            elif command == "poprzedni":
                spotify.previous_track()
                message = 'Cofnięto do poprzedniego utworu'
            
            # Search
            elif command == "wyszukaj":
                song_uri = spotify.search(text, 1)
                print(song_uri)

            # Output message
            # if response.status_code == 204:
            #     print(startingSpace + F"(TTS) {message}")
            #     if tts('pl', message) == 3: print(ctrlCMsg)

            # Connection error

# Ctrl + C handling
except KeyboardInterrupt:
    print(ctrlCMsg)

# Critical error handling
