import os
import sys

# Operacny system 
print(os.uname())



from machine import UART
import sys

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, pins=('P4','P3'), timeout_chars=5)

while True:
    a= uart.readline()
    if a:
        a = str(a).replace('b','').replace('\'','')
        if a[0] == '$' and a[len(a)-4:] == "\\r\\n":
            a = a[:len(a)-4]
            print (a)
