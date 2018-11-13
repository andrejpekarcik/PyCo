import os
import sys

#
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


from machine import UART
import sys
import time

#uart = UART(1, 9600)
#uart.init(9600, bits=8, parity=None, stop=1, pins=('P4','P3'), timeout_chars=5)

uartSigfox = UART(0, 9600)
uartSigfox.init(9600, bits=8, parity=None, stop=1, pins=('P22','P23'))

while True:

    uartSigfox.write('\r\nAT$SF=FF1234567890CC')
    time.sleep(1)
    if (uartSigfox.any()>0):
        print (uartSigfox.readln())




#while True:
#    a= uart.readline()
#
#    NMEA , NMEA_stav = NMEAchecksum (a)
#    if NMEA_stav:
#        if 'GPRMC' in NMEA:
#            print(NMEA)
##            veta = NMEA.split(',')
#            print (veta)
#            print (veta[0])
