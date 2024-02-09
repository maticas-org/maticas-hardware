#include "Event.h"

Event::Event() {
    type_ = -1; // Initialize with an unknown type
    statusCode_ = -1;
    timestamp_ = "";
    data_ = "";
}

Event::Event(int type, int statusCode, const String& timestamp, const String& data) {
    type_ = type;
    statusCode_ = statusCode;
    timestamp_ = timestamp;
    data_ = data;
}

int Event::getType() const {
    return type_;
}

int Event::getStatusCode() const {
    return statusCode_;
}

String Event::getTimestamp() const {
    return timestamp_;
}

String Event::getData() const {
    return data_;
}

void Event::setTimestamp(const String& timestamp) {
    timestamp_ = timestamp;
}


String Event::toString() const {

    //json like string representation
    String eventString = "{";
    eventString += "\"type\":";
    eventString += type_;
    eventString += ",\"statusCode\":";
    eventString += statusCode_;
    eventString += ",\"timestamp\":\"";
    eventString += timestamp_;
    eventString += "\",\"data\":\"";
    eventString += data_;
    eventString += "\"}";

    return eventString;
}

bool Event::operator==(const Event& other) const {
    return (type_ == other.type_ && statusCode_ == other.statusCode_ && timestamp_ == other.timestamp_ && data_ == other.data_);
}

bool Event::operator!=(const Event& other) const {
    return !(*this == other);
}
