#ifndef ADAPTER_H
#define ADAPTER_H

#include <Arduino.h>
#include "Target.h"
#include "Adaptee.h"
#include "Event.h"

class Adapter : public Target, public Adaptee {
public:
    void setSpecificRequest(Event (*specificRequestFunc)());
    Event request() override;

private:
    Event (*specificRequestFunc)();
};

#endif // ADAPTER_H
