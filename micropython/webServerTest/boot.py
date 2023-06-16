try:
  import usocket as socket
except:
  import socket

from time                   import sleep
from machine                import Pin
from internet_connection    import *

import gc
import esp
import network

esp.osdebug(None)
gc.collect()
sleep(3)

connect2(config_file = "config.json", doreconnect = True)
