#!/bin/bash

echo ! CONFIGURING BASE SYSTEM !

sudo pacman-mirrors --api --set-branch testing
sudo pacman-mirrors --fasttrack 5 
sudo pacman -Syy linux-rpi4-mainline linux-rpi4-mainline-headers --noconfirm
sudo pacman -Sy mpg123 spotifyd neofetch python-pip git base-devel

sudo mkdir /spotify-cache
sudo cp ./spotifyd-config.conf /etc/spotifyd.conf
sudo loginctl enable-linger $USER
systemctl --user enable spotifyd.service

sudo pacman -Syu
git clone https://aur.archlinux.org/yay-bin
cd yay-bin
makepkg -si --noconfirm
cd ..
rm -rf yay-bin

yay -Sy python-pyaudio --noconfirm
pip install gTTS pydexcom SpeechRecognition