#GROWMATIC V2.0
print "Growmatic v2.0"
import time
time.sleep(1)
print "Firing up engines"
time.sleep(2)
# IMPORT DEVICES
print "Importing devices"
time.sleep(2)
import Adafruit_BMP.BMP085 as BMP085
import PCF8591 as ADC
#import LCD1602
import RPi.GPIO as GPIO
import datetime
import math

DHTPIN = 17
DO = 13

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5
print "Checking Time"
print "CONFIRM TIME BEFORE CONNECTING"
print time.strftime("      %a %d-%m-%Y @ %H:%M:%S")
time.sleep(3)

#GPIO/ADC SETUP
print "Loading GPIO"
time.sleep(1)
print "Loading ADC"
time.sleep(1)
def read_dht11_dat():
        GPIO.setup(DHTPIN, GPIO.OUT)
        GPIO.output(DHTPIN, GPIO.OUT)
        ADC.setup(0x48)
        GPIO.setup      (DO,    GPIO.IN)
        #LCD1602.init(0x27, 1)
        GPIO.output(DHTPIN, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(DHTPIN, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)
        unchanged_count = 0
        last = -1
        data = []
        while True:
                current = GPIO.input(DHTPIN)
                data.append(current)
                if last != current:
                        unchanged_count = 0
                        last = current
                else:
                        unchanged_count += 1
                        if unchanged_count > MAX_UNCHANGE_COUNT:
                                break
        state = STATE_INIT_PULL_DOWN
        lengths = []
        current_length = 0
        for current in data:
                current_length += 1

                if state == STATE_INIT_PULL_DOWN:
                        if current == GPIO.LOW:
                                state = STATE_INIT_PULL_UP
                        else:
                                continue
                if state == STATE_INIT_PULL_UP:
                        if current == GPIO.HIGH:
                                state = STATE_DATA_FIRST_PULL_DOWN
                        else:
                                continue
                if state == STATE_DATA_FIRST_PULL_DOWN:
                        if current == GPIO.LOW:
                                state = STATE_DATA_PULL_UP
                        else:
                                continue
                if state == STATE_DATA_PULL_UP:
                        if current == GPIO.HIGH:
                                current_length = 0
                                state = STATE_DATA_PULL_DOWN
                        else:
                                continue
                if state == STATE_DATA_PULL_DOWN:
                        if current == GPIO.LOW:
                                lengths.append(current_length)
                                state = STATE_DATA_PULL_UP
                        else:
                                continue
        if len(lengths) != 40:
                return False
        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0
        for length in lengths:
                bit = 0
                if length > halfway:
                        bit = 1
                bits.append(bit)
        for i in range(0, len(bits)):
                byte = byte << 1
                if (bits[i]):
                        byte = byte | 1
                else:
                        byte = byte | 0
                if ((i + 1) % 8 == 0):
                        the_bytes.append(byte)
                        byte = 0
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
                return False

        return the_bytes[0], the_bytes[2]

#MAIN SCRIPT
print "Running Main Script..."
time.sleep(0.2)
print  "ALL OK"
def main():
        status = 1
        moi = 1
        while True:
                result = read_dht11_dat()
                if result:
                        humidity, temperature = result
                        #LCD1602.write (0,1, str("Hum="))
                        #LCD1602.write (4,1, str(humidity))
                        csvresult = open("/home/pi/humidity.csv","a")
                        csvresult.write(str(humidity) + "," + "\n")
                        #LCD1602.write (7,1, str("Temp="))
                        #LCD1602.write (12,9, str(temperature))
                        csvresult = open("/home/pi/temperature.csv","a")
                        csvresult.write(str(temperature) + "," + "\n")
                analogVal = ADC.read(0)
                Vr = 5 * float(analogVal) / 255
                Rt = 10000 * Vr / (5 - Vr)
                moist = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15)))
                moist = moist - 273.15
                #LCD1602.write (0,0, str("Moist="))
                #LCD1602.write (7,0, str(moist))
                csvresult = open("/home/pi/moisture.csv","a")
                csvresult.write(str(moist) + "," + "\n")
                sensor = BMP085.BMP085()
                temp = sensor.read_temperature()
                pressure = sensor.read_pressure()
                #LCD1602.write (3,0, str("temp="))
                #LCD1602.write (9,0, str(pressure))
                csvresult = open("/home/pi/temp.csv","a")
                csvresult.write(str(temp) + "," + "\n")
                csvresult = open("/home/pi/pressure.csv","a")
                csvresult.write(str(pressure) + "," + "\n")
                tmp = GPIO.input(DO)
                csvresult = open("/home/pi/gas.csv","a")
                csvresult.write(str(tmp) + "," + "\n")
                if tmp != status:
                        status = tmp
                else:
                        count = 0
                time.sleep(1)

#CLEANUP
def destroy():
        GPIO.cleanup()

if __name__ == '__main__':
        try:
                main()
        except KeyboardInterrupt:
                destroy() 