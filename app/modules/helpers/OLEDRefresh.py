# Import libraries
import os, json, colorama
colorama.init()

# Script directory
script_dir=os.path.dirname(os.path.realpath(__file__))

# Default message starts
infoMsg = colorama.Fore.GREEN + "[OLED] " + colorama.Style.RESET_ALL
warningMsg = colorama.Fore.YELLOW + "[OLED] " + colorama.Style.RESET_ALL
errorMsg = colorama.Fore.RED + "[OLED] " + colorama.Style.RESET_ALL
ctrlCMsg = "\n" + infoMsg + "Użyto" + colorama.Fore.RED + " Ctrl + C" + colorama.Style.RESET_ALL + ", wyjście do nadrzędnego skryptu"
   
def OLEDRefresh(text="Słucham..."):
    try: 
         # Import required packages
        import board, displayio, terminalio, adafruit_displayio_ssd1306
        from adafruit_display_text import label

        # Open settings file
        with open(script_dir + '/../../settings.json') as f:
            settings = json.load(f)["GPIO"]["OLEDScreen"]
        border=5

        # Initialize screen
        displayio.release_displays()
        i2c = board.I2C()
        display_bus = displayio.I2CDisplay(i2c, device_address=settings["address"])
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=settings["width"], height=settings["height"])

        if not display: return

        splash = displayio.Group()
        display.show(splash)
        color_bitmap = displayio.Bitmap(settings["width"], settings["height"], 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF

        # Draw text
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        inner_bitmap = displayio.Bitmap(settings["width"]-border*2, settings["height"]-border*2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000 # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=border, y=border)
        splash.append(inner_sprite)

        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=settings["height"]//2-1)
        splash.append(text_area)

        display.show(displayio.Group())
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=settings["height"]//2-1)

    # Ctrl + C clicked
    except KeyboardInterrupt:
        print(ctrlCMsg)
        return 3
    
    # Critical error
    except:
        print(errorMsg + "Inizjalizacja OLED nieudana")
        return False