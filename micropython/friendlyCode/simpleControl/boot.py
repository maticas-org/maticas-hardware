from time import sleep
from utils.internet_connection import *

config_file = "utils/config.json"

#sleep 3 seconds before starting
sleep(3)

#connects to internet
connect2(config_file = config_file, doreconnect = False)

#sleep 3 seconds after starting connection
sleep(3)


