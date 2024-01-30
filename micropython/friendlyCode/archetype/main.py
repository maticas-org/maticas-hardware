import machine
from src.time_event_manager          import *
from src.internet_connection_manager import *

from src.sensor_adapters               import *
from src.sensors_micro_service         import *
from src.data_management_micro_service import *


#----------------- EventManager instances -----------------#
TIME_UPDATE_INTERVAL: int = 5 #seconds
rtc  = machine.RTC()

time_event_manager = TimeEventManager(rtc, TIME_UPDATE_INTERVAL)
conn_event_manager = ConnectionEventManager("config_file.json")

#----------------- Subscriber instances -----------------#
sensors_micro_service         = SensorsMicroService()
data_management_micro_service = DataManagementMicroService("config_file.json")

time_event_manager.subscribe(sensors_micro_service)
sensors_micro_service.subscribe(data_management_micro_service)
conn_event_manager.subscribe(data_management_micro_service)

#----------------- Sensor instances -----------------#
dummy_sensor = DummyAdapter()
dht11_sensor = DHT11Adapter(pin=4, read_n_times=5)

#----------------- Add sensors to SensorsMicroService -----------------#
sensors_micro_service.add_sensor(dummy_sensor)
sensors_micro_service.add_sensor(dht11_sensor)

#----------------- Run business logic -----------------#
time_event_manager.notify()
conn_event_manager.notify()

#----------------- Run business logic periodically -----------------#
timer = machine.Timer(0)
timer.init(period=TIME_UPDATE_INTERVAL*1000, mode=machine.Timer.PERIODIC, callback=lambda t: time_event_manager.notify())