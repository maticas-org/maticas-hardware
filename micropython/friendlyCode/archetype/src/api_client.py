import urequests as requests
import ujson

class ApiClient:

    def __init__(self, 
                 config_file: str) -> None:

        self.config_file = config_file

        with open(config_file) as f:
            self.config_file = ujson.load(f)
            self.config_file = self.config_file['wifi']
    
    def send_data(self,
                  data: dict) -> None:
            """
                Sends data to the cloud.
                If it fails, raises an exception.
            """
            print('ApiClient sending data to cloud...')
            print('Data: {}'.format(data))
            print('Sending data to: {}'.format(self.config_file['api_url']))

            maximum_wait_time = 7.5 #seconds
            try:
                response = requests.post(self.config_file['api_url'], 
                                        json=data, 
                                        timeout=maximum_wait_time)
            except Exception as e:

                #if it's due to timeout
                if 'timed out' in str(e):
                    print('Error sending data to cloud: {}'.format(e))
                    return
                
                #if it's due to internet connection or OS error 113 
                if ('EHOSTUNREACH' in str(e)) or (e.args[0] == 113):
                    print('Error sending data to cloud: {}'.format(e))
                    return

                raise Exception('Error sending data to cloud.', e)

            else:
                print('Response: {}'.format(response.text))

                if response.status_code >= 300:
                    raise Exception('Error when data sent to cloud got {} status code.'.format(response.status_code))

                print('Data sent to cloud.')

import os 
from src.dependencies import sdcard
from machine import Pin, SPI 
spi = SPI(2)
spi.init()
sd = sdcard.SDCard(spi, Pin(5))
vfs = os.VfsFat(sd)

os.mount(vfs, '/sd')
files = os.listdir('/sd')