from .event import *

class EventManager():

    subscribers = []

    def __init__(self) -> None:
        self.first_event:Event = None
        self.last_event:Event = None

    def get_first_event(self) -> Event:
        return self.first_event
    
    def subscribe(self, subscriber: "Subscriber") -> None:
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: "Subscriber") -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        for subscriber in self.subscribers:
            subscriber.update(self.last_event)

    def main(self) -> None:
        #some previous business logic
        #...
        self.notify()