from network import LTE
​
print(os.uname())

pass

lte = LTE()
print (lte.send_at_cmd('AT+CFUN=0'))
print (lte.send_at_cmd('AT!="clearscanconfig"'))
print (lte.send_at_cmd('AT!="addscanband band=20"'))
print (lte.send_at_cmd('AT!="disablelog 1"'))
print (lte.send_at_cmd('AT+CGDCONT=1,"IP","hologram"'))
print (lte.send_at_cmd('AT+CFUN=1'))

while not lte.isattached():
    print ('net')
    pass
​
lte.connect()
while not lte.isconnected():
    print ('da')
    pass
​
