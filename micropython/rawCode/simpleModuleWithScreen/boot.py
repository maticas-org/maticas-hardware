from time import sleep
from utils.internet_connection import*
from utils.json_related import*
config_file="utils/config.json"
sleep(3)
ip=connect2(config_file=config_file,doreconnect=False)
update_json_file(config_file,"ip",ip)
sleep(3)