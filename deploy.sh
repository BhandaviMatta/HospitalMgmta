#comment
#creating web deploying script
#!bin/bash
sudo apt update -y
sudo apt install zip unzip -y
sudo apt install nginx -y
sudo rm -r /var/www/html
sudo git clone https://github.com/BhandaviMatta/HospitalMgmta.git /var/www/html

