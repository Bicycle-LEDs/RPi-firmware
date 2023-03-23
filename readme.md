# 🪄 Speech recognition program for Raspberry Pi or PC in Python

## ✨ To configure Raspberry:
1. Install manjaro arm minimal and do some basic config
2. Install git (`pacman -Sy git --noconfirm`)
3. Clone this repo (`git clone https://github.com/Bicycle-LEDs/RPi-firmware`)
4. Run `sh RPi-firmware/config/system-setup.sh` 

⚠️ This will move your manjaro branch to *testing*, change kernel to *linux-rpi4-mainline*, install yay, install stuff required to run this project

## ⚡ To run this project:
1. Clone this repo (`git clone https://github.com/Bicycle-LEDs/RPi-firmware`) *make sure you have **git** installed*
2. Make sure you have `portaudio` (or `libportaudio19-dev`) installed (**for linux only**)
3. Install requirements (skip this step if used Raspberry configurator) (`sh RPi-firmware/config/meet-requirements.sh`)
4. Run script: ```python launch.py```