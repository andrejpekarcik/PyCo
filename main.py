import pycoco,os
import sys
import pycom

from network import Sigfox
import socket
from machine import UART
import time
import deepsleep

# Sigfox sigfox_inicializacia
#
def sigfox_init(a):

    global s

    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    s.setblocking(True)

    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    return s

print(os.uname())
print ('----------------')

sigfox_init(0)
s.send(11)

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
