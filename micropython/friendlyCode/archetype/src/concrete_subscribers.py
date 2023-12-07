from .event import *
from .subscriber import *
from .event_manager import *

class SensorsMicroService(Subscriber, EventManager):

    subscribers = []

    def __init__(self):

        self.sensors = []

        self.last_time_event: Event             = None 
        self.first_measurement_event: EventList = None
        self.last_measurement_event: EventList  = None

    #----------------- EventManager interface -----------------#
    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def notify(self):
        
        #run business logic
        self.main()
        print('SensorsMicroService notifying subscribers...')

        #notify subscribers
        for subscriber in self.subscribers:
            subscriber.update(self.last_measurement_event)

    def main(self):
        print('SensorsMicroService running business logic...')
            
        measurement_event_list = EventList()
        
        #read sensors
        for sensor in self.sensors:
            measurement_event = sensor.request()
            measurement_event_list.extend(measurement_event)
            
        #update the timestamp of the measurement events
        for event in measurement_event_list:
            event.data['timestamp'] = self.last_time_event.timestamp
            event.timestamp = self.last_time_event.timestamp

        if self.first_measurement_event == None:
            self.first_measurement_event = measurement_event_list

        self.last_measurement_event = measurement_event_list

    #----------------- Subscriber interface -----------------#
    def update(self, event: Event):
        print('\nSensorsMicroService got event: "{}"'.format(event))

        if event.type != TIME_EVENT:
            raise TypeError('Cannot handle event of type {}'.format(event.type))

        self.last_time_event = event
        self.notify()
    

    #----------------- Business logic -----------------#
    def add_sensor(self, sensor):
        print('SensorsMicroService adding sensor...')
        self.sensors.append(sensor)

    def remove_sensor(self, sensor):
        print('SensorsMicroService removing sensor...')
        self.sensors.remove(sensor)


class DataManagementMicroService(Subscriber):

    def __init__(self):
        self.last_measurement_event: EventList = None
        self.last_connection_event: Event      = None

    #----------------- Subscriber interface -----------------#
    def update(self, event: Event):
        print('\nDataManagementMicroService got event: "{}"'.format(event))

        if event.type == MEASUREMENT_EVENT:
            self.last_measurement_event = event
            self.main()
        elif event.type == CONNECTION_EVENT:
            self.last_connection_event = event
            self.main()
        else:
            raise TypeError('Cannot handle event of type {}'.format(event.type))

    #----------------- Business logic -----------------#
    def main(self):
        print('DataManagementMicroService running business logic...')

        if self.last_measurement_event == None or self.last_connection_event == None:
            return

        if self.last_connection_event.data['status'] == 'connected':
            print('DataManagementMicroService sending data to cloud...')
        else:
            print('DataManagementMicroService storing data locally...')