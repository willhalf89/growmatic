_________________________________________________________________________________________________________________

BUILD + INSTALL GROWMATIC 2.0
-----------------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------------
PINS:
-----------------------------------------------------------------------------------------------------------------
Use Balena etcher to copy latest "Raspbian Buster Lite" image to SD.
-----------------------------------------------------------------------------------------------------------------

https://www.balena.io/etcher/

https://www.raspberrypi.org/downloads/raspbian/

-----------------------------------------------------------------------------------------------------------------
Edit and copy Wifi and SSH files to "boot" partition.
-----------------------------------------------------------------------------------------------------------------

https://github.com/willhalf89/growmatic/raw/master/RPI%20Headless.zip

-----------------------------------------------------------------------------------------------------------------
Boot Pi.
-----------------------------------------------------------------------------------------------------------------

sudo raspi-config

ENABLE SPI

ENABLE I2C

CHANGE TIMEZONE

-----------------------------------------------------------------------------------------------------------------
Install Prerequisites 
-----------------------------------------------------------------------------------------------------------------

sudo apt-get -y update

sudo apt-get -y install build-essential python-pip python-dev python-smbus git

cd ~

sudo pip install --upgrade setuptools pip

sudo reboot now

------------------------------------------------------------------------------------------------------------------
Python Script + PCF8591 + ADC BMP180
------------------------------------------------------------------------------------------------------------------

(Copy/Paste All)

wget https://raw.githubusercontent.com/willhalf89/growmatic/master/growmatic.py

wget https://raw.githubusercontent.com/sunfounder/SunFounder_SensorKit_for_RPi2/master/Python/PCF8591.py

sudo git clone https://github.com/adafruit/Adafruit_Python_BMP.git

cd Adafruit_Python_BMP

sudo python setup.py install

sudo rm setuptools-3.5.1.zip

sudo wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.5.1.zip

sudo python setup.py install

sudo pip install s3cmd

cd ~

sudo git clone https://github.com/adafruit/Adafruit_Python_GPIO.git

cd Adafruit_Python_GPIO

sudo python setup.py install

cd ~

------------------------------------------------------------------------------------------------------------------
InfluxDB
------------------------------------------------------------------------------------------------------------------

(RUN AS ONE COMMAND)

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -

source /etc/os-release

echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt update && sudo apt install -y influxdb

sudo systemctl unmask influxdb.service

sudo systemctl start influxdb

sudo systemctl enable influxdb.service

sudo reboot now

influx

create database Growmatic

use Growmatic

create user grafana with password 'awesome89' with all privileges

grant all privileges on Growmatic to grafana

exit

sudo reboot now

------------------------------------------------------------------------------------------------------------------
Grafana
------------------------------------------------------------------------------------------------------------------

sudo apt-get install -y adduser libfontconfig1

wget https://dl.grafana.com/oss/release/grafana-rpi_6.7.3_armhf.deb

sudo dpkg -i grafana-rpi_6.7.3_armhf.deb

sudo systemctl unmask grafana-server.service

sudo systemctl start grafana-server

sudo systemctl enable grafana-server.service

(EDIT CONFIG)

sudo nano /etc/grafana/grafana.ini

[auth]

#disable_login_form = false 

disable_login_form = true

Change disable_login_form to true.

Enable anonymous access:

[auth.anonymous]

enabled = true

Specify the organization:

org_name = YOUR_ORG_NAME_HERE

org_role = Editor

sudo reboot now

------------------------------------------------------------------------------------------------------------------
Node-Red
------------------------------------------------------------------------------------------------------------------

bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

sudo systemctl enable nodered.service

sudo reboot now

------------------------------------------------------------------------------------------------------------------
NOTES:
------------------------------------------------------------------------------------------------------------------
Grafana :3000

Node-Red :1880

Node-Red Dashboard UI :1880/ui

Nodes:

dashboard

gate

ui_led

ui_valuetrail

influxdb

SAMPLE NODE RED JSON:
