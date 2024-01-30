#ifndef EVENT_MANAGER_H
#define EVENT_MANAGER_H

#include <Arduino.h>
#include <vector>
#include "Event.h"
#include "Subscriber.h"

/*
* The EventManager class is responsible for managing events and notifying subscribers.
*/
class EventManager {
public:
    EventManager();
    Event getFirstEvent();
    void subscribe(Subscriber* subscriber);
    void unsubscribe(Subscriber* subscriber);
    virtual void notify();
    virtual void main();

protected:
    Event firstEvent;
    Event lastEvent;
    std::vector<Subscriber*> subscribers;
};

#endif // EVENT_MANAGER_H
