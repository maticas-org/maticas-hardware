#ifndef ADAPTEE_H
#define ADAPTEE_H

#include <Arduino.h>

class Adaptee {
public:
    virtual Event specificRequest() = 0;
};

#endif // ADAPTEE_H