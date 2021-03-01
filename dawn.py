!/usr/bin/env python
from yeelight import *
import time
import sys

bulb = Bulb("192.168.0.117")
bulb.turn_on()

interval=sys.argv[1]
interval=int(interval)

for  i in range(1,101):
        bulb.set_brightness(i)
        print("Brightness was set to ")
        print(i)
        time.sleep(interval/100)
