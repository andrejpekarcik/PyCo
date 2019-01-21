import os
import sys
import pycom
from network import Sigfox
import socket
from machine import UART
import time

__version__ = '1.0.0'

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



# spracuje vystup zo NMEAchecksum a vrati GPS polohu
# vystup: sirka, dlzka, sever/juh, vychod/zapad
#

def NMEA_poloha (NMEA_veta):
    if 'GPRMC' in NMEA:
        veta = NMEA.split(',')
        stav = veta[2]
        sirka = veta[3].replace('.','')[:10]
        dlzka = veta[5].replace('.','')[:10]

        #print (stav, sirka, dlzka, len (sirka), len (dlzka))
        #print (sirka + dlzka)

        if stav == 'A':
            return sirka, dlzka, True







# Odvysiela sigfox spravu najviac 14 bajtov
#
def sigfox_poslat (sprava,s):
    s.send(sprava)
