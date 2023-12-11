from src.time_event_manager          import *
from src.internet_connection_manager import *

from src.sensor_adapters               import *
from src.sensors_micro_service         import *
from src.data_management_micro_service import *

#----------------- EventManager instances -----------------#
rtc  = None

time_event_manager = TimeEventManager(rtc=rtc)
conn_event_manager = ConnectionEventManager("config_file.json")

#----------------- Subscriber instances -----------------#
sensors_micro_service         = SensorsMicroService()
data_management_micro_service = DataManagementMicroService("config_file.json")

time_event_manager.subscribe(sensors_micro_service)
sensors_micro_service.subscribe(data_management_micro_service)
conn_event_manager.subscribe(data_management_micro_service)

#----------------- Sensor instances -----------------#
dummy_sensor = DummyAdapter()

#----------------- Add sensors to SensorsMicroService -----------------#
sensors_micro_service.add_sensor(dummy_sensor)

#----------------- Run business logic -----------------#
time_event_manager.notify()
conn_event_manager.notify()