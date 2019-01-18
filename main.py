import pycoco,os
import sys
import pycom

from network import Sigfox
import socket
from machine import UART
import time
import deepsleep



print ('zxc', pycoco.ZLTA)

#print(os.uname())
#print ('----------------')

pycoco.sigfox_init(0)
pycoco.sigfox_poslat(123)

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(pycoco.cervena)

#  UART pre GPS start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pc.rgbled(zlta)

print ('--SiPy------------------------------------------------------------------')

while True:
    a = uart.readline()
    NMEA , NMEA_stav = pycoco.NMEAchecksum (a)
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
                pycom.rgbled(pycoco.zelena)
                #sigfox_poslat (sirka)
                time.sleep(5)
                pycoco.sigfox_poslat(sirka)
                pycoco.sigfox_poslat(dlzka)

                time.sleep (40)
            else:
                pycom.rgbled(pycoco.modra)
