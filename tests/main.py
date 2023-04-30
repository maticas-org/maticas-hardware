import urequests
import re
from machine import Pin
from time 	 import sleep

relay = Pin(25, Pin.OUT)

def parse_datetime_time(datetime_str):
    
    start = 11
    end = -7
    
    txt = datetime_str.strip()
    txt = txt[start:end]
    time_str = txt.split(":")
    
    print(time_str)
    hour = int(time_str[0])
    minute = int(time_str[1])
    second = float(time_str[2])
    
    return hour, minute, second

def on_off_cycle():

    response = urequests.get('http://worldtimeapi.org/api/timezone/America/Bogota')

    if (response.status_code == 200):
        parsed  = response.json()
        h, m, s = parse_datetime_time(parsed["datetime"])
        
        if (h > 20) or (h < 6):
            relay.value(0)
        else:
            relay.value(1)
    sleep(1)
    
while True:
    
    on_off_cycle()
    sleep(4)



        


