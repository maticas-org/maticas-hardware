from src.concrete_event_manager import *
from src.concrete_subscribers import *
from src.concrete_adapters import *

#----------------- EventManager instances -----------------#
rtc  = None
conn = None

time_event_manager = TimeEventManager(rtc=rtc)
conn_event_manager = ConnectionEventManager(conn=conn)


#----------------- Subscriber instances -----------------#
sensors_micro_service = SensorsMicroService()
time_event_manager.subscribe(sensors_micro_service)


#----------------- Sensor instances -----------------#
dummy_sensor = DummyAdapter()

#----------------- Add sensors to SensorsMicroService -----------------#
sensors_micro_service.add_sensor(dummy_sensor)


#----------------- Run business logic -----------------#
time_event_manager.notify()
conn_event_manager.notify()