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
    WiFiClient client;
    ApiClient apiClient = ApiClient(client);


public:
    int measurementEventsCount = 0;
    Event measurementEvents[MAX_MEASUREMENTS];

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
    }

    /*
    * Flushes the events array
    */
    void flushEvents(){
        Serial.println("Flushing events...");
        measurementEventsCount = 0;
        for (int i = 0; i < MAX_MEASUREMENTS; i++){
            measurementEvents[i] = Event();
        }
    }

    /*
    * Sends the pending data to the server
    */
    void sendPendingData(){
        Serial.println("Sending pending [allocated in mem] data...");
        int* statusCodes = apiClient.sendEvents(measurementEvents, measurementEventsCount);
        // some events can be sent successfully, others not
        // if the event was sent successfully, remove it from the array and decrement the count
        // and move the events so that the array is compacted (no empty spaces in the middle)
        for (int i = 0; i < measurementEventsCount; i++){
            if (statusCodes[i] == OK_STATUS || statusCodes[i] == CREATED_STATUS){
                for (int j = i; j < measurementEventsCount - 1; j++){
                    measurementEvents[j] = measurementEvents[j + 1];
                }
                measurementEventsCount--;
            }
        }

        // fill the empty spaces with empty events
        for (int i = measurementEventsCount; i < MAX_MEASUREMENTS; i++){
            measurementEvents[i] = Event();
        }
    }

    //------------------------ Subscriber Interface ------------------------
    void update(const Event* events, int size) override {
        // make sure size is not greater than MAX_MEASUREMENTS
        if (size > MAX_MEASUREMENTS){
            Serial.printf("WARNING: Size of events array is greater (%d) than MAX_MEASUREMENTS. Truncating to %d\n", size, MAX_MEASUREMENTS);
            size = MAX_MEASUREMENTS;
        }

        // if the first event is not a measurement event then 
        // can be assumed that the incoming array is an error
        if (events[0].getType() != MEASUREMENT_EVENT){
            Serial.println("First event is not a measurement event. Ignoring incoming events...");
            return;
        }

        Serial.printf("ConnectionEventManager received an array of %d events...\n", size);
        int* statusCodes = apiClient.sendEvents(events, size);

        
        // add the remainig events to the measurementEvents array (the ones that were not sent successfully)
        // if the array is full, the oldest event is removed (first in first out)
        for (int i = 0; i < size; i++){
            
            // if the data was sent successfully, do not add it to the measurementEvents array
            if (statusCodes[i] != OK_STATUS && statusCodes[i] != CREATED_STATUS){
                //if the array is full, remove the oldest event, otherwise, increment the count
                //and add the event to the array
                if (measurementEventsCount == MAX_MEASUREMENTS){
                    for (int j = 0; j < MAX_MEASUREMENTS - 1; j++){
                        measurementEvents[j] = measurementEvents[j + 1];
                    }
                    measurementEvents[MAX_MEASUREMENTS - 1] = events[i];
                } else {
                    measurementEvents[measurementEventsCount] = events[i];
                    measurementEventsCount++;
                }
            }
        }

        logMemoryUsage();
    }

    //does the same as the update method, but is adapted to the EventArray struct
    //which comes from the loadEventsFromSD method in the DataManagementMicroService
    void updateFromLoadedEvents(EventArray& events) {
        Serial.printf("ConnectionEventManager received an array from SD of %d events...\n", events.size);

        if (events.size > MAX_MEASUREMENTS){
            Serial.printf("WARNING: Size of events array is greater (%d) than MAX_MEASUREMENTS. Truncating to %d\n", events.size, MAX_MEASUREMENTS);
            events.size = MAX_MEASUREMENTS;
        }else if (events.size == 0){
            Serial.println("No events to update");
            return;
        }
        
        update(events.events, events.size);
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
