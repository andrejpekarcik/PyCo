import os
import sys
import pycom
#import Pylib
from network import Sigfox
import socket
from machine import UART
import time
import deepsleep
import Pylib
from Pylib import NMEAchecksum

cervena = 0x7f0000
zelena = 0x00FF00
modra = 0x0000FF
zlta = 0x7f7f00
# Overi ci NMEA veta a checksum sedia, vracia True, False
#


# Operacny system zobrazit
print(os.uname())
print ('----------------')


# sigfox start
global s
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(cervena)

#  UART pre GPS start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pycom.rgbled(zlta)

print ('--SiPy--------------------------')

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
