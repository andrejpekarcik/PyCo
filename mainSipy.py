import os
import sys
import pycom
import Pylib
from network import Sigfox
import socket
from machine import UART
import time

cervena = 0x7f0000
zelena = 0x00FF00
modra = 0x0000FF
zlta = 0x7f7f00
# Overi ci NMEA veta a checksum sedia, vracia True, False
#

def NMEAchecksum(NMEA_veta):

    # odstranim ' a 'b'
    NMEA_veta = str(NMEA_veta).replace('b','').replace('\'','')
    # kontrolujem $ a \r\n na konci
    if NMEA_veta[0] != '$' or NMEA_veta[len(NMEA_veta)-4:] != "\\r\\n":
        return None,False
    # \r\n sa odsekne
    NMEA_veta = NMEA_veta[:len(NMEA_veta)-4]
    # kontrola poctu * a ci je * tri znaky od konca
    if NMEA_veta.count('*') != 1 or NMEA_veta[len(NMEA_veta)-3] != '*':
        return None,False
    # ak je na zaciatku $ tak sa odstrani
    if NMEA_veta[0] == "$":
        NMEA_veta = NMEA_veta.replace('$','')
    # rozdelim na vetu a checksum
    NMEA_veta,NMEA_checksum = NMEA_veta.split('*')

    # vypocitame checksum
    NMEA_checksum_calculated = 0
    for char in NMEA_veta:
        NMEA_checksum_calculated ^= ord(char)

    # ak checksum nesedi tak False
    if hex(NMEA_checksum_calculated)[2:] != NMEA_checksum:
        return None, False

    return NMEA_veta,True

# Odvysiela sigfox spravu najviac 14 bajtov
#
def sigfox_poslat (sprava):
    if len (sprava) % 2 == 1:
        sprava = sprava + '0'
    s.send(sprava)


# Sigfox sigfox_inicializacia
#
def sigfox_inicializacia():
    #
    global s
​    # init Sigfox for RCZ1 (Europe)
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
​    # create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
​    # make the socket blocking
    s.setblocking(True)
​    # configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
​
# Operacny systemmain
print(os.uname())
print ('----------------')

# sigfox start
sigfox_inicializacia()
sigfox_poslat('1')

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(cervena)

#  UART start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pycom.rgbled(zlta)

print ('--mainSiPy--------------------------')

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
