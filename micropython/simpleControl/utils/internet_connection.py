import network
import utime

from json    import load

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



def connect2(config_file: str, doreconnect = False) -> None:
    with open(config_file) as f:
        config = load(f)

    sta_if = network.WLAN(network.STA_IF) # create station interface
    ap_if = network.WLAN(network.AP_IF) # create access-point interface

    # Disconnect AP if it is up and de-activate the AP interface
    ap_if.active(False) 
    utime.sleep(1)

    # Connect to WiFi hotspot if not already connected
    if not sta_if.isconnected():
        print('Connecting to hotspot...')
        sta_if.active(True)
        sta_if.connect(config["wifi_ssid"], config["wifi_password"])

        # Wait up to 600 seconds (10 minutes) for connection to succeed
        for count in range(600):
            if sta_if.isconnected():
                print('Network config:', sta_if.ifconfig())
                return sta_if
            print('.', end='')
            utime.sleep(1)

        # Disconnect and de-activate STA interface if connection fails
        sta_if.disconnect()
        sta_if.active(False)
        print('Connection failed')

    else:
        # Print interface configuration data if already connected
        print('Already connected')
        print('Network config:', sta_if.ifconfig())
        
        if doreconnect:
            print('Reconnecting ...')
            reconnect(config_file, sta_if)
            
        

def reconnect(config_file: str, sta_if: network.WLAN) -> None:
    # Disconnect and de-activate STA interface
    sta_if.disconnect()
    sta_if.active(False)
    print('Disconnecting from network...')

    # Reconnect to WiFi hotspot
    connect2(config_file, doreconnect = False)



