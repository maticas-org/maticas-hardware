import ubinascii
import network

def get_mac_address():

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    mac = ubinascii.hexlify(wlan_mac).decode().upper()

    #formats the mac address to be more readable with the usual colon seperation
    mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))

    return mac

print(get_mac_address())
