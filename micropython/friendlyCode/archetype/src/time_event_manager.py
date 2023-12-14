from .abstractions.event import * 
from .abstractions.subscriber import Subscriber
from .abstractions.event_manager import EventManager

class TimeEventManager(EventManager):

    subscribers = []

    def __init__(self, rtc) -> None:
        self.first_time_event:Event = None
        self.last_time_event:Event = None
        self.rtc = rtc

        print('Initialized TimeEventManager.')

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
        data = dict()
        data["time"] = "14:2:02"
        time_event = Event(TIME_EVENT, OK_STATUS, data["time"], data)

        if self.first_time_event is None:
            self.first_time_event = time_event

        self.last_time_event = time_event