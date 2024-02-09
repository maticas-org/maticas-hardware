#ifndef EVENT_H
#define EVENT_H

#include <Arduino.h>

// Define event types
#define TIME_EVENT 0
#define CONNECTION_EVENT 1
#define MEASUREMENT_EVENT 2
#define RAM_EVENT 3
#define UNKNOWN_EVENT -1

// Define event status codes
#define OK_STATUS 200
#define BUG_RESILIENCE_STATUS 299
#define BAD_REQUEST_STATUS 400
#define UNAUTHORIZED_STATUS 401
#define FORBIDDEN_STATUS 403
#define NOT_FOUND_STATUS 404
#define INTERNAL_SERVER_ERROR 500
#define NOT_IMPLEMENTED_STATUS 501
#define SERVICE_UNAVAILABLE_STATUS 503

class Event {
public:
    Event();
    Event(int type, int statusCode, const String& timestamp, const String& data);
    
    int getType() const;
    int getStatusCode() const;
    String getTimestamp() const;
    String getData() const;
    void setTimestamp(const String& timestamp);
    String toString() const;

    // Comparison operators
    bool operator==(const Event& other) const;
    bool operator!=(const Event& other) const;

private:
    int type_;
    int statusCode_;
    String timestamp_;
    String data_;
};

#endif // EVENT_H