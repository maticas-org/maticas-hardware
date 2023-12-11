from .event import *

class Subscriber():
    def __init__(self):
        pass

    def update(self, event: Event):
        print('{} got message "{}"'.format(event))

        if event.type == TIME_EVENT:
            print('Time event: {}'.format(event.timestamp))
        
        if event.type == CONNECTION_EVENT:
            print('Connection event: {}'.format(event.value))

    