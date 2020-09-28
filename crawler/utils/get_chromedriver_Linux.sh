#!/bin/bash

echo "Install Chrome..."

# https://superuser.com/questions/1475553/running-selenium-on-wsl-using-chrome
chrome_linux='https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
wget $chrome_linux
sudo dpkg -i google-chrome*.deb
sudo apt -f -y install
sudo dpkg -i google-chrome*.deb

echo "Installing ChromeDriver..."

chrome_driver_linux='https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip'
wget $chrome_driver_linux
unzip chromedriver*.zip
