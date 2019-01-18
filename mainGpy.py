import os
import sys
import pycom
import Pylib

cervena = 0x7f0000
zelena = 0x00FF00
modra = 0x0000FF
zlta = 0x7f7f00

# Odvysiela sigfox spravu najviac 14 bajtov
#

def sigfox_poslat (sprava):
    if len (sprava) % 2 == 1:
        sprava = sprava + '0'
    msg = '\r\nAT$SF=' + sprava
    print (msg)
    if len(msg) < 6:
        return
    uart.write(msg)





# Operacny system
print(os.uname())

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(cervena)

from machine import UART
import sys
import time

#  UART start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pycom.rgbled(zlta)

print ('ads')

while True:
    a = uart.readline()
    NMEA , NMEA_stav = NMEAchecksum (a)
    if NMEA_stav:
        if 'GPRMC' in NMEA:
            print(NMEA)
            veta = NMEA.split(',')
            print (veta)
            stav = veta[2]
            sirka = veta[3].replace('.','')[:10]
            dlzka = veta[5].replace('.','')[:10]

            print (stav, sirka, dlzka, len (sirka), len (dlzka))
            print (sirka + dlzka)

            if stav == 'A':
                pycom.rgbled(zelena)
                #sigfox_poslat (sirka)
                time.sleep(5)
                sigfox_poslat(sirka)
                sigfox_poslat(dlzka)

                time.sleep (40)
            else:
                pycom.rgbled(modra)
    else:
            pycom.rgbled(modra)
