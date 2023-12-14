import utime
import usocket
import network
from json import load

from .abstractions.event import * 
from .abstractions.subscriber import Subscriber
from .abstractions.event_manager import EventManager


class ConnectionEventManager(EventManager):

    subscribers = []

    def __init__(self, config_file: str) -> None:
        self.first_connection_event: Event = None
        self.last_connection_event:  Event = None
        self.config_file: str = config_file
        print('Initialized ConnectionEventManager.')

    def get_first_event(self) -> Event:
        return self.first_connection_event
    
    def subscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        #run business logic
        self.main()
        print('ConnectionEventManager notifying subscribers...')

        #notify subscribers
        for subscriber in self.subscribers:
            subscriber.update(self.last_connection_event)

    def main(self) -> None:
            
        print('\nConnectionEventManager running business logic...')
        
        if self.last_connection_event is None:
            self.connect()

        elif self.last_connection_event.status == SERVICE_UNAVAILABLE_STATUS:
            self.connect(doreconnect = True)

        elif self.last_connection_event.status == OK_STATUS:
            self.ping()

        else:
            message = "Unhandled connection status code: {}".format(self.last_connection_event.status)
            raise UnhandledStatusCode(message)
            

    def connect(self,
                doreconnect = False) -> Event:
        """
            Connects to the internet using the credentials
            stored in the config file.

            Args:
                doreconnect (bool): If True, it will try to reconnect to the internet
                                    even if it is already connected. Default is False.

            Returns:
                Event: The ip address of the device.
        """
        with open(self.config_file) as f:
            config = load(f)

        wifi_ssid = config["wifi"]["ssid"]
        wifi_pass = config["wifi"]["password"]

        self.sta_if = network.WLAN(network.STA_IF) # create station interface
        self.ap_if = network.WLAN(network.AP_IF) # create access-point interface

        # Disconnect AP if it is up and de-activate the AP interface
        self.ap_if.active(False) 
        utime.sleep(1)

        # Connect to WiFi hotspot if not already connected
        if (not self.sta_if.isconnected()) or (self.last_connection_event is None):

            try:
                print('Connecting to hotspot...')
                self.sta_if.active(True)
                self.sta_if.connect(wifi_ssid, wifi_pass)

                # Wait up to 600 seconds (10 minutes) for connection to succeed
                for count in range(600):
                    if self.sta_if.isconnected():

                        print('Network config:', self.sta_if.ifconfig())
                        return self.ping()

                    print('.', end='')
                    utime.sleep(1)

                # Disconnect and de-activate STA interface if connection fails
                self.sta_if.disconnect()
                self.sta_if.active(False)
                print('Connection failed')

            except OSError as e:
                self.last_connection_event = Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", {"error": str(e)})
                return self.last_connection_event

        else:
            # Print interface configuration data if already connected
            print('Already connected')
            print('Network config:', self.sta_if.ifconfig())
            
            if doreconnect:
                print('Reconnecting ...')
                return self.reconnect(self.sta_if)

            else: 
                return self.last_connection_event

    def reconnect(self,
                  sta_if: network.WLAN) -> None:

        # Disconnect and de-activate STA interface
        sta_if.disconnect()
        sta_if.active(False)
        print('Disconnecting from network...')

        # Reconnect to WiFi hotspot
        return self.connect(doreconnect = False)


    def ping(self,
             count: int = 4,
             threshold: float = 0.33) -> Event:

        with open(self.config_file) as f:
            config = load(f)

        hosts = config["wifi"]["ping_urls"]

        try:
            from src.dependencies import uping

            for host in hosts:
                print("Pinging {}...".format(host))

                ntransmited, nrecieved = uping.ping(host, count=count)
                ratio = nrecieved/ntransmited

                if ratio >= threshold:
                    print("Ping to {} successful!".format(host))
                    data = {"ping": "successful"}
                    data["host"] = host
                    data["ntransmited"] = ntransmited
                    data["nrecieved"] = nrecieved
                    self.last_connection_event = Event(CONNECTION_EVENT, OK_STATUS, "", data)

                    return self.last_connection_event       

        except Exception as e:
            raise e

        else:   

            # If none of the hosts were reachable
            data = {"ping": "failed"}
            data["host"] = hosts
            self.last_connection_event = Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", data)

            return self.last_connection_event