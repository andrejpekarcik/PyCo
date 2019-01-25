import pyco
import os
import sys
import pycom
from deepsleep import DeepSleep
import deepsleep
from machine import Timer
import time

from network import Sigfox
import socket
from machine import UART
import time

# Kolko ma hlboko spat medzi cas medzi meraniami v sekundach
cas_medzi_meraniami = 3600

# Pauza pred meranim GPS
pauza_pred_GPS = 0.1

# Ako dlho sa ma pokusat precitat GPS v sekundach
max_cas_pre_gps = 300

print ('-SiPy start------------------------------------------------------------')

ds = DeepSleep()
stopky_pre_GPS = Timer.Chrono()

sigfox = pyco.sigfox_init()

# Vypnut LED
pycom.heartbeat(False)
pycom.rgbled(pyco.cervena)

#  UART pre GPS start
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P23','P22'), timeout_chars=5)

pycom.rgbled(pyco.zlta)

print ('--SiPy------------------------------------------------------------------')

while True:

    lap = stopky_pre_GPS.read()
    time.sleep(pauza_pred_GPS)

    if (lap == 0):
        print ("sama nula")
        stopky_pre_GPS.start()

    if (lap > max_cas_pre_gps):
        stopky_pre_GPS.stop()
        ds.go_to_sleep(cas_medzi_meraniami)

    print (lap)

    raw_gps_data = uart.readline()
    NMEA , NMEA_stav = pyco.NMEAchecksum (raw_gps_data)

    if NMEA_stav:
        sirka, dlzka, poloha_stav = pyco.NMEA_poloha (NMEA)
        print ("Poloha stav:",poloha_stav)
        if poloha_stav:
            pycom.rgbled(pyco.zelena)
            pyco.sigfox_posli(sirka)
            pyco.sigfox_posli(dlzka)
            stopky_pre_GPS.stop()
            ds.go_to_sleep(cas_medzi_meraniami)
        else:
            pycom.rgbled(pyco.modra)
