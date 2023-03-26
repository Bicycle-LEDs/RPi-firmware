#!/bin/bash

echo ! CONFIGURING BASE SYSTEM !

echo "FONT=Lat2-Terminus16" | sudo tee -a /etc/vconsole.conf
echo "FONT_MAP=8859-2" | sudo tee -a /etc/vconsole.conf
sudo pacman-mirrors --api --set-branch testing
sudo pacman-mirrors --fasttrack 5 
sudo pacman -Sy mpg123 portaudio spotifyd neofetch python-pip git base-devel alsa-utils i2c-tools lm_sensors qrencode --noconfirm

sudo mkdir /spotify-cache
sudo loginctl enable-linger $USER
systemctl --user enable spotifyd.service

sudo pacman -Syu --noconfirm
git clone https://aur.archlinux.org/yay-bin
cd yay-bin
makepkg -si --noconfirm
cd ..
rm -rf yay-bin

sh ./install.sh