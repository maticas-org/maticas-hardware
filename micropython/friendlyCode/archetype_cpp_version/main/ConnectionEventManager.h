#ifndef CONNECTION_EVENT_MANAGER_H
#define CONNECTION_EVENT_MANAGER_H

#include <Arduino.h>
#include <WiFi.h> // Include the appropriate WiFi library for your board

#include "CustomUtils.h"
#include "Event.h"
#include "Subscriber.h"
#include "EventManager.h"
#include "ApiClient.h"

#define MAX_MEASUREMENTS 30

class ConnectionEventManager : public EventManager, public Subscriber{
private:
    Event firstConnectionEvent;
    Event lastConnectionEvent;
    Event measurementEvents[MAX_MEASUREMENTS];
    WiFiClient client;
    ApiClient apiClient = ApiClient(client);


public:

    ConnectionEventManager() {
        firstConnectionEvent = Event(CONNECTION_EVENT, SERVICE_UNAVAILABLE_STATUS, "", "{\"error\":\"No connection events yet\"}");
        lastConnectionEvent = firstConnectionEvent;

        for (int i = 0; i < MAX_MEASUREMENTS; i++){
            measurementEvents[i] = Event();
        }
    }

    Event getFirstEvent() {
        return firstConnectionEvent;
    }

    //------------------------ Event Manager Interface ------------------------
    void notify() override {
        // Run business logic
        main();
        Serial.println("ConnectionEventManager notifying subscribers...");

        // Notify subscribers
        for (int i = 0; i < number_of_subs; i++){
            subscribers_[i]->update(lastEvent);
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

        //if there are unsent measurement events, send them to the subscribers
        Serial.println("Checking for unsent measurement events...");
        for (int i = 0; i < MAX_MEASUREMENTS; i++){
            if (measurementEvents[i].getType() == MEASUREMENT_EVENT){
                for (int j = 0; j < number_of_subs; j++){
                    subscribers_[j]->update(measurementEvents[i]);
                }
                measurementEvents[i] = Event();
            }
        }

    }

    //------------------------ Subscriber Interface ------------------------
    void update(const Event& event) override {
        Serial.println("ConnectionEventManager received an event...");
        
        if (event.getType() == MEASUREMENT_EVENT){
            Serial.println("Received a measurement event");
            int statusCode = apiClient.sendEvent(event);
        
            if (statusCode == 200) {
                Serial.println("Event sent successfully");
            } else {
                Serial.println("Failed to send event");
            }
        }else{
            Serial.println("Received a non-measurement event");
            std::runtime_error("Received a non-measurement event");
        }

    }

    void update(const Event* events, int size) override {
        Serial.printf("ConnectionEventManager received an array of %d events...\n", size);

        bool firstTime   = false;
        int unsentEvents = 0;
        int* statusCodes = apiClient.sendEvents(events, size);
        
        // Create a new array of events to store the remaining events
        Event remainingEvents[size];
        

        // Check the status codes of the events and store the remaining events
        for (int i = 0; i < size; i++){
            if (statusCodes[i] != 200) {
                remainingEvents[i] = events[i];
                remainingEvents[i].timesSent++;
                unsentEvents++;
            }else{
                remainingEvents[i] = Event();
            }
        }

        //get the first event that was not sent and check if it is the first time
        for (int i = 0; i < unsentEvents; i++){
            if (remainingEvents[i].getType() == MEASUREMENT_EVENT){
                firstTime = remainingEvents[i].timesSent == 1;
                Serial.println("First time: " + String(firstTime));
                Serial.println("Event: " + remainingEvents[i].toString());
                break;
            }
        }

        logMemoryUsage();

        /*
        * May need to add async logic to handle unsent events, this is because the ESP32 
        * has a limited amount of memory and may not be able to handle all the events at once
        * and seems to have problems with nested loops and calls, for example, 
        * in this scenario dataManagementMicroService.notify() calls the update method of
        * the ConnectionEventManager, which calls the update method of the subscribers 
        * (and dataManagementMicroService is a subscriber of ConnectionEventManager)
        */

        // Notify subscribers if the timesSent attribute of the remaining events is 1 
        // meaning that the event was sent for the first time, and if there are unsent events

        if (unsentEvents > 0 && firstTime){
            Serial.println("There are unsent events and it is the first time");
            for (int i = 0; i < number_of_subs; i++){
                subscribers_[i]->update(remainingEvents, unsentEvents);
            }
        } else if (unsentEvents > 0){
            Serial.println("There are unsent events but it is not the first time");

            //leave the notification for the next time
            for (int i = 0; i < unsentEvents; i++){
                if (remainingEvents[i].getType() == MEASUREMENT_EVENT){
                    measurementEvents[i] = remainingEvents[i];
                }
            }

        } else {
            Serial.println("There are no unsent events");
        }
    }

    //------------------------ Business Logic ------------------------
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
