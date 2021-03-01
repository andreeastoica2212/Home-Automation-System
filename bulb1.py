#!/usr/bin/env python
from yeelight import *
import time
import paho.mqtt.client as mqtt
import socket

bulb = Bulb("192.168.0.117")
username = "openhabian"
password = "parola"
topic = "/bulb1/command/#"

def find_localhost():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        broker = s.getsockname()[0]
        s.close()
        return broker

def on_connect(client,userdata,flags,rc):
        if rc==0:
                print("Subscribing to all topics!")
                client.subscribe(topic)
        else:
                print("Bad connection returned code= ",rc)

def on_message_power(client,userdata,msg):
        if (msg.payload == "1"):
                bulb.turn_on()
        elif (msg.payload == "0"):
                bulb.turn_off()
        print("Power was set!")

def on_message_brightness(client, userdata, msg):
        bulb.set_brightness(int(msg.payload))
        print("Brightness was set!")

def on_message_color(client, userdata, msg):
        r = msg.payload.split(',')[0] 
        g = msg.payload.split(',')[1] 
        b = msg.payload.split(',')[2] 
        bulb.set_rgb(int(r),int(g),int(b))      
        print("Color was set!")

def on_message_temperature(client, userdata, msg):
        temp = int(msg.payload)
        temp = temp*6500/100
        bulb.set_color_temp(temp)
        print("Temp was set!")  

broker = find_localhost()
client=mqtt.Client()

print("Connecting to Openhab")
client.username_pw_set(username,password)
client.connect(broker)

client.on_connect = on_connect

client.message_callback_add('/bulb1/command/power', on_message_power)
client.message_callback_add('/bulb1/command/brightness', on_message_brightness)

client.message_callback_add('/bulb1/command/color', on_message_color)
client.message_callback_add('/bulb1/command/temperature', on_message_temperature)

client.loop_forever()