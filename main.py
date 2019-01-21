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
    raw_gps_data = uart.readline()
    NMEA , NMEA_stav = pyco.NMEAchecksum (raw_gps_data)
    if NMEA_stav:
        poloha_stav = pyco.NMEA_poloha (NMEA)
        print (poloha_stav)
        if poloha_stav == 'A':
            pycom.rgbled(pyco.zelena)
            time.sleep(5)
            pyco.sigfox_poslat(sirka)
            pyco.sigfox_poslat(dlzka)
            time.sleep (40)
        else:
            pycom.rgbled(pyco.modra)
