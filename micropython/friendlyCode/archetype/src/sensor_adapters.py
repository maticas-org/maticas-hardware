from time import sleep

from .abstractions.adapter import Adapter
from .abstractions.event import *

class DummyAdapter(Adapter):

    def __init__(self) -> None:
        print('Initialized DummyAdapter.')
        pass

    def specific_request(self) -> EventList:
        print('\tDummyAdapter running business logic...')
        event_list = EventList()
        event_list.append(Event(MEASUREMENT_EVENT, OK_STATUS, '', {'timestamp': '', 'ambient variable': 0}))
        return event_list

    def request(self) -> EventList:
        return self.specific_request()


class DHT11Adapter(Adapter):

    def __init__(self, pin: int, read_n_times: int = 5) -> None:
        from dht import DHT11

        self.dht = DHT11(pin)
        self.read_n_times = read_n_times

    def specific_request(self) -> EventList:
        
        #read temperature and humidity n times
        temperature = 0
        humidity = 0
        count = 0

        for _ in range(self.read_n_times):
            self.dht.measure()
            temp_measurement = self.dht.temperature()
            humidity_measurement = self.dht.humidity()

            if self.validate_measurement(temp_measurement) and self.validate_measurement(humidity_measurement):
                temperature += temp_measurement
                humidity += humidity_measurement
                count += 1
            sleep(1)
            
        temperature /= self.read_n_times
        humidity /= self.read_n_times

        #create events
        temperature_event = Event(MEASUREMENT_EVENT, OK_STATUS, '', {'timestamp': '', 'temperature': temperature})
        humidity_event    = Event(MEASUREMENT_EVENT, OK_STATUS, '', {'timestamp': '', 'humidity': humidity})

        return EventList([temperature_event, humidity_event])

    def request(self) -> EventList:
        return self.specific_request()

    def validate_measurement(self, measurement_value: float) -> bool:
        return measurement_value > 0 and measurement_value < 100