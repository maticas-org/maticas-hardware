#ifndef CONNECTION_EVENT_MANAGER_H
#define CONNECTION_EVENT_MANAGER_H

#include <Arduino.h>
#include <WiFi.h> // Include the appropriate WiFi library for your board

#include "Event.h"
#include "Subscriber.h"
#include "EventManager.h"

class ConnectionEventManager : public EventManager {
private:
    Event firstConnectionEvent;
    Event lastConnectionEvent;
    WiFiClient client;

public:
    ConnectionEventManager() {
        firstConnectionEvent = Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", "{\"error\":\"No connection events yet\"}");
        lastConnectionEvent = firstConnectionEvent;
    }

    Event getFirstEvent() {
        return firstConnectionEvent;
    }

    void notify() override {
        // Run business logic
        main();
        Serial.println("ConnectionEventManager notifying subscribers...");

        // Notify subscribers
        for (Subscriber* subscriber : subscribers) {
            subscriber->update(lastConnectionEvent);
        }
    }

    void main() override {
        Serial.println("\nConnectionEventManager running business logic...");

        if (lastConnectionEvent.getStatusCode() >= 500){
            Serial.println("Connection status code is 500 or greater ");
            connect();
        } else if (lastConnectionEvent.getStatusCode() == SERVICE_UNAVAILABLE_STATUS) {
            Serial.println("Connection status code is " + String(SERVICE_UNAVAILABLE_STATUS));
            connect(true);
        } else if (lastConnectionEvent.getStatusCode() == OK_STATUS) {
            Serial.println("Connection status code is " + String(OK_STATUS));
            lastConnectionEvent = check_connection();
        } else {
            String message = "Unhandled connection status code: " + String(lastConnectionEvent.getStatusCode());
            Serial.println(message);
            throw std::runtime_error(message.c_str());
        }
    }

    void connect(bool doReconnect = false) {

        // Disconnect if already connected
        WiFi.disconnect();

        // Connect to WiFi hotspot if not already connected
        if (!WiFi.isConnected() || lastConnectionEvent.getType() == -1) {
            Serial.println("Connecting to hotspot...");
            WiFi.begin(MY_SSID, MY_PASSWORD);

            // Wait up to 600 seconds (10 minutes) for connection to succeed
            for (int count = 0; count < 600; count++) {
                if (WiFi.status() == WL_CONNECTED) {
                    Serial.println("Connected to WiFi");
                    Serial.print("IP Address: ");
                    Serial.println(WiFi.localIP());
                    lastConnectionEvent = Event(CONNECTION_EVENT, OK_STATUS, "", "{\"error\":\"Succesfully connected to WiFi\"}"); 
                    return;
                }
                Serial.print(".");
                delay(1000);
            }

            // If connection fails, set the event accordingly
            lastConnectionEvent = Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", "{\"error\":\"Connection failed\"}");
        } else {
            // Already connected
            Serial.println("Already connected");
            if (doReconnect) {
                Serial.println("Reconnecting...");
                reconnect();
            }
        }
    }

    void reconnect() {
        // Disconnect and reconnect to WiFi
        WiFi.disconnect();
        delay(1000);
        return connect(false);
    }

    Event check_connection(){
        // Check connection
        if (!client.connect("www.google.com", 80)) {
            Serial.println("Connection failed");
            return Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", "{\"error\":\"Connection failed\"}");
        } else {
            Serial.println("Connection successful");
            return Event(CONNECTION_EVENT, OK_STATUS, "", "{\"error\":\"Connection successful\"}");
        }
    }

};



#endif // CONNECTION_EVENT_MANAGER_H
