import gc
from time import sleep
from utils.internet_connection import *
from utils.json_related import update_json_field

config_file = "utils/config.json"

#sleep 3 seconds before starting
sleep(3)

#connects to internet
ip = connect2(config_file = config_file, doreconnect = False)
update_json_field(config_file, "ip", ip)

#sleep 3 seconds after starting connection
sleep(3)
gc.collect()