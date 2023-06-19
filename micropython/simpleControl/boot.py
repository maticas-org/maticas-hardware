from time import sleep
from internet_connection import *

#sleep 3 seconds before starting
sleep(3)

#connects to internet
connect2(config_file = "config.json", doreconnect = True)

#sleep 3 seconds after starting connection
sleep(3)
