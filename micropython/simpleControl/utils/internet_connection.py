import network
import utime

def connect(config_file: str)-> None:

    # reads the configuration file and stores it in a dictionary
    # for later instantiation of the connection
    with open(config_file) as f:
        config = load(f)

    count  = 0
    sta_if = network.WLAN(network.STA_IF) # create station interface
    ap_if  = network.WLAN(network.AP_IF) #  create access-point interface

    #  disconnects AP if it is up
    #  de-activate the AP interface
    ap_if.active(False) 

    utime.sleep(1)

    if not sta_if.isconnected():

        print('connecting to hotspot...')
        sta_if.active(True)
        sta_if.connect(config["wifi_ssid"], config["wifi_password"])

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
        if (sta_if.isconnected()):  #  maybe not necessary
            sta_if.disconnect()
        sta_if.active(False)        #  this is necessary

    count = 0 #  reset count
    utime.sleep(1)

