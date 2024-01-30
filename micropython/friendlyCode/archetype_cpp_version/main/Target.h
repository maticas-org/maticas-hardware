#ifndef TARGET_H
#define TARGET_H

#include <Arduino.h>
#include "Event.h"

class Target {
public:
    virtual Event request() = 0;
};

#endif // TARGET_H