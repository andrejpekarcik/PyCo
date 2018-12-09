import os
import sys
import pycom

cervena = 0x7f0000
zelena = 0x00FF00
modra = 0x0000FF
zlta = 0x7f7f00

# Odvysiela sigfox spravu najviac 14 bajtov
#

def sigfox_poslat (sprava):
    msg = '\r\nAT$SF=' + sprava
    uart.write(msg)


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

sigfox_poslat('')
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
            sirka = veta[3].replace('.','')
            dlzka = veta[5].replace('.','')

            print (stav, sirka, dlzka)
            print (sirka + dlzka)

            if stav == 'A':
                pycom.rgbled(zelena)
                sigfox_poslat (sirka + dlzka)
                time.sleep (500)
            else:
                pycom.rgbled(modra)
    else:
            pycom.rgbled(modra)
