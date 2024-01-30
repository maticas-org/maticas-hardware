#include "Adapter.h"
#include "Event.h"

void Adapter::setSpecificRequest(Event (*specificRequestFunc)()) {
    this->specificRequestFunc = specificRequestFunc;
}

Event Adapter::request() {
    return specificRequestFunc();
}
