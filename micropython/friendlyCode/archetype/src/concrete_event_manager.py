from .event import *
from .subscriber import Subscriber
from .event_manager import EventManager

class TimeEventManager(EventManager):

    subscribers = []

    def __init__(self, rtc) -> None:
        self.first_time_event:Event = None
        self.last_time_event:Event = None
        self.rtc = rtc

        print('TimeEventManager initialized.')

    def get_first_event(self) -> Event:
        return self.first_time_event

    def subscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        #run business logic
        self.main()
        print('TimeEventManager notifying subscribers...')

        #notify subscribers
        for subscriber in self.subscribers:
            subscriber.update(self.last_time_event)

    def main(self):
    
        print('\nTimeEventManager running business logic...')
        time_event = Event(TIME_EVENT, TIME_EVENT, TIME_EVENT, dict())

        if self.first_time_event is None:
            self.first_time_event = time_event

        self.last_time_event = time_event

    
class ConnectionEventManager(EventManager):

    subscribers = []

    def __init__(self, conn) -> None:
        self.first_connection_event:Event = None
        self.last_connection_event:Event = None
        self.conn = conn
        print('ConnectionEventManager initialized.')

    def get_first_event(self) -> Event:
        return self.first_connection_event
    
    def subscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber: Subscriber) -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        #run business logic
        self.main()
        print('ConnectionEventManager notifying subscribers...')

        #notify subscribers
        for subscriber in self.subscribers:
            subscriber.update(self.last_connection_event)

    def main(self) -> None:
            
        print('\nConnectionEventManager running business logic...')
        connection_event = Event(CONNECTION_EVENT, CONNECTION_EVENT, CONNECTION_EVENT, dict())
            
        if self.first_connection_event is None:
            self.first_connection_event = connection_event

        self.last_connection_event = connection_event
