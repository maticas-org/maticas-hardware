# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import utime
import machine



sta_if = network.WLAN(network.STA_IF) # create station interface
ap_if = network.WLAN(network.AP_IF) #  create access-point interface

def connect():
    count = 0

    #  disconnects AP if it is up
    #  de-activate the AP interface
    ap_if.active(False) 

    utime.sleep(1)

    if not sta_if.isconnected():
        print('connecting to hotspot...')
        sta_if.active(True)
        sta_if.connect("LinuxEsAmor", "nuncaheusadoarch")

        while (count < 5):
            count += 1

            if (sta_if.isconnected()):
                count = 0
                print (' network config:', sta_if.ifconfig())
                break

            print ('.', end = '')
            utime.sleep(1)


    if (count == 5):
     #  disconnect or you get errors
        if (sta_if.isconnected()): #  maybe not necessary
            sta_if.disconnect()

        sta_if.active(False) #  this is necessary

    count = 0 #  reset count

    utime.sleep(1)
    
connect()

