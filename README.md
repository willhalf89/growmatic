-----------------------------------------------------------------------------------------------------------------
_________________________________________________________________________________________________________________

BUILD + INSTALL GROWMATIC 2.0
_________________________________________________________________________________________________________________

-----------------------------------------------------------------------------------------------------------------

PINS:

-----------------------------------------------------------------------------------------------------------------
1) Use Balena etcher to copy latest "Raspbian Buster Lite" image to SD.
-----------------------------------------------------------------------------------------------------------------

https://www.balena.io/etcher/

https://www.raspberrypi.org/downloads/raspbian/

-----------------------------------------------------------------------------------------------------------------
2) Edit and copy Wifi and SSH files to "boot" partition.
-----------------------------------------------------------------------------------------------------------------

https://github.com/willhalf89/growmatic/raw/master/RPI%20Headless.zip

-----------------------------------------------------------------------------------------------------------------
3) Boot Pi.
-----------------------------------------------------------------------------------------------------------------

sudo raspi-config

ENABLE SPI

ENABLE I2C

CHANGE LOCALE

CHANGE TIMEZONE

sudo reboot now

------------------------------------------------------------------------------------------------------------------
4) Python Script
------------------------------------------------------------------------------------------------------------------

wget https://github.com/willhalf89/growmatic/blob/master/growmatic.py

------------------------------------------------------------------------------------------------------------------
5) PCF8591 ADC + BMP180
------------------------------------------------------------------------------------------------------------------

wget https://github.com/sunfounder/SunFounder_SensorKit_for_RPi2/blob/master/Python/PCF8591.py

sudo apt-get update

sudo apt install git-all

git clone https://github.com/sunfounder/Adafruit_Python_BMP.git

cd Adafruit_Python_BMP

sudo python setup.py install

------------------------------------------------------------------------------------------------------------------
6) Node-Red
------------------------------------------------------------------------------------------------------------------

bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

sudo systemctl enable nodered.service

sudo reboot now

------------------------------------------------------------------------------------------------------------------
7) InfluxDB + Grafana
------------------------------------------------------------------------------------------------------------------

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install -y influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

influx

create database Growmatic

use Growmatic

create user grafana with password 'awesome89' with all privileges

grant all privileges on Growmatic to grafana

exit

sudo reboot now

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update && sudo apt install -y grafana

sudo systemctl unmask grafana-server.service

sudo systemctl start grafana-server

sudo systemctl enable grafana-server.service

sudo reboot now

------------------------------------------------------------------------------------------------------------------
NOTES:
------------------------------------------------------------------------------------------------------------------
Grafana :3000
Node-Red :1880
Node-Red Dashboard UI :1880/ui
