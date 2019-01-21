import pyco
import os
import sys
import pycom

from network import Sigfox
import socket
from machine import UART
import time

print ('-SiPy start------------------------------------------------------------')

sigfox = pyco.sigfox_init()
pyco.sigfox_posli ('9999')

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(pyco.cervena)

#  UART pre GPS start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pycom.rgbled(pyco.zlta)

print ('--SiPy------------------------------------------------------------------')

while True:
    a = uart.readline()
    NMEA , NMEA_stav = pyco.NMEAchecksum (a)
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
                pycom.rgbled(pyco.zelena)
                #sigfox_poslat (sirka)
                time.sleep(5)
                pyco.sigfox_poslat(sirka)
                pyco.sigfox_poslat(dlzka)

                time.sleep (40)
            else:
                pycom.rgbled(pyco.modra)
