from .abstractions.event import * 
from .abstractions.subscriber import Subscriber
from .abstractions.event_manager import EventManager

class TimeEventManager(EventManager):

    subscribers = []

    def __init__(self,
                 rtc,
                 default_time_update_interval_secs: int) -> None:

        self.first_time_event:Event = None
        self.last_time_event:Event = None
        self.rtc = rtc
        self.update_interval_secs = default_time_update_interval_secs

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
        
        try:
            (Y, M, D, wd, h, m, sec, subsec) =  self.rtc.datetime()

            data["timestamp"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(Y, M, D, h, m, sec)
            time_event = Event(TIME_EVENT, OK_STATUS, data["timestamp"], data)

        except Exception as e1:
            import sys
            import uio
            print('Error on RTC read: ', e1)
            sys.print_exception(e1)
            
            #work around RTC failure
            try:
                time_event = self.work_around_rtc_failure()
            
            except Exception as e2:
                s1 = uio.StringIO()
                sys.print_exception(e1, s1)
                exception_string = s1.getvalue()
                
                raise Exception("Error during work around RTC failure: ", e2, Exception("Handling error from: ", exception_string))
            
        if self.first_time_event is None:
            self.first_time_event = time_event

        self.last_time_event = time_event
        print("\tupdate: ", self.last_time_event.data["timestamp"])

    def work_around_rtc_failure(self):
        last_timestamp = self.last_time_event.data["timestamp"]
        
        #split the timestamp into date and time
        date = last_timestamp.split(' ')[0]
        time = last_timestamp.split(' ')[1]

        #split the date into year, month and day
        Y, M, D = [int(t) for t in date.split('-')]

        #split the time into hour, minute and second
        h, m, s = [int(t) for t in time.split(':')]
        
        #increment by the update interval, considering the overflow
        s += self.update_interval_secs
        m += s // 60
        s %= 60

        h += m // 60
        m %= 60

        D += h // 24
        h %= 24

        M += D // 30
        D %= 30

        Y += M // 12
        M %= 12

        #reconstruct the timestamp
        data = dict()
        data["timestamp"] = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(Y, M, D, h, m, s)

        #create the event
        time_event = Event(TIME_EVENT, BUG_RESILIENCE_STATUS, data["timestamp"], data)
        return time_event