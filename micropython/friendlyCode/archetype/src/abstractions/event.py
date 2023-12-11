# Event types
TIME_EVENT         = 0
CONNECTION_EVENT   = 1
MEASUREMENT_EVENT  = 2
RAM_EVENT          = 3

# Event status codes
OK_STATUS = 200

BAD_REQUEST_STATUS  = 400
UNAUTHORIZED_STATUS = 401
FORBIDDEN_STATUS    = 403
NOT_FOUND_STATUS    = 404

INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED_STATUS = 501
SERVICE_UNAVAILABLE_STATUS = 503


class Event():

    def __init__(self, type_: int, status_code: int, timestamp: str, data: dict) -> None:

        self.type        = type_
        self.status_code = status_code
        self.timestamp   = timestamp
        self.data        = data

    def __str__(self) -> str:
        return f'{self.type} {self.status_code} {self.timestamp} {self.data}'

    def __repr__(self) -> str:
        return f'{self.type} {self.status_code} {self.timestamp} {self.data}'

    def __eq__(self, other) -> bool:
        
        if isinstance(other, Event):
            return self.type == other.type and self.status_code == other.status_code and self.timestamp == other.timestamp and self.data == other.data
        elif other == None:
            return False
        else:
            raise TypeError('Cannot compare Event with {}'.format(type(other)))

    def __ne__(self, other) -> bool:

        if isinstance(other, Event):
            return not self.__eq__(other)
        else:
            raise TypeError('Cannot compare Event with {}'.format(type(other)))


class EventList():

    def __init__(self) -> None:
        self.queue = []

    def append(self, event: Event) -> None:
        self.queue.append(event)

    def extend(self, other) -> None:  
        self.__add__(other)

    def __str__(self) -> str:
        return str(self.queue)

    def __repr__(self) -> str:
        return str(self.queue)

    def __setitem__(self, index: int, event: Event) -> None:
        self.queue[index] = event

    def __add__(self, other) -> None:
        if not isinstance(other, EventList):
            raise TypeError('Cannot add EventList with {}'.format(type(other)))

        self.queue.extend(other.queue)

    def __eq__(self, other) -> bool:
            
        if isinstance(other, EventList):
            return self.queue == other.queue
        elif other == None:
            return False
        else:
            raise TypeError('Cannot compare EventList with {}'.format(type(other)))

    def __ne__(self, other) -> bool:

        if not isinstance(other, EventList):
            raise TypeError('Cannot compare EventList with {}'.format(type(other)))

        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(self.queue)

    def __getitem__(self, index: int) -> Event:
        return self.queue[index]