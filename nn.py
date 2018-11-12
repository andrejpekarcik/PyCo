from network import LTE

import time
​

print(os.uname())

lte = LTE()
print (lte.send_at_cmd('AT+CGDCONT=1,"IP","hologram"'))
print (lte.attach(band=20))

while not lte.isattached():
	print('Attaching…')
	time.sleep(0.25)



lte.connect()
