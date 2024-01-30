#include "EventManager.h"

/*
* The EventManager class is responsible for managing events and notifying subscribers.
*/
EventManager::EventManager() {
    firstEvent = Event();
    lastEvent = Event();
}

Event EventManager::getFirstEvent() {
    return firstEvent;
}

void EventManager::subscribe(Subscriber* subscriber) {
    subscribers.push_back(subscriber);
}

void EventManager::unsubscribe(Subscriber* subscriber) {
    // Find and remove the subscriber
    for (size_t i = 0; i < subscribers.size(); i++) {
        if (subscribers[i] == subscriber) {
            subscribers.erase(subscribers.begin() + i);
            break;
        }
    }
}

void EventManager::notify() {
    for (Subscriber* subscriber : subscribers) {
        subscriber->update(lastEvent);
    }
}

void EventManager::main() {
    Serial.println("Executing business logic...");
    // Some previous business logic...
    // ...
    Serial.println("Done! Notifying subscribers...");
    notify();
}
