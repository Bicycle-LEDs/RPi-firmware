#!/bin/bash

echo ! CONFIGURING BASE SYSTEM !

sudo pacman-mirrors --api --set-branch testing
sudo pacman-mirrors --fasttrack 5 
sudo pacman -Syy linux-rpi4-mainline linux-rpi4-mainline-headers --noconfirm
sudo pacman -Sy neofetch python-pip git base-devel
sudo pacman -Syu
git clone https://aur.archlinux.org/yay-bin
cd yay-bin
makepkg -si --noconfirm
cd ..
rm -rf yay-bin
yay -Sy python-pyaudio --noconfirm
pip install gTTS pydexcom SpeechRecognition