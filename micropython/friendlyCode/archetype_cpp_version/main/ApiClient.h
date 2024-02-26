#ifndef API_CLIENT_H
#define API_CLIENT_H

#include <WiFi.h> // Include the appropriate WiFi library for your board
#include <Arduino.h>
#include <ArduinoHttpClient.h>
#include "secrets.h"
#include "Event.h"


#define MAX_MEASUREMENTS 30
class ApiClient {

    private:
        HttpClient http_;
        int last_results[MAX_MEASUREMENTS];

    public:

        ApiClient(WiFiClient &client) : http_(client, API_URL, API_PORT) {
            reset_last_results();
            http_.setHttpResponseTimeout(HTTP_TIMEOUT);
        }

        int sendEvent(const Event& event) {
            // Send event to server
            Serial.println("Sending event to server...");
            String contentType = "application/json";
            String postData = event.getData();

            http_.connectionKeepAlive();
            http_.beginRequest();
            http_.post(API_ENDPOINT);
            http_.sendHeader("Content-Type", contentType);
            http_.sendHeader("Content-Length", postData.length());
            http_.sendHeader("Custom-Header", "custom");
            http_.beginBody();
            http_.print(postData);
            http_.endRequest();

            int statusCode = http_.responseStatusCode();
            String response = http_.responseBody();

            if (statusCode == 0){
                Serial.println("Success Sending event");
                statusCode = http_.responseStatusCode();

                if (statusCode >= 0) {
                    String response = http_.responseBody();
                    Serial.println("Status code: " + String(statusCode));
                    Serial.println("Body length: " + http_.contentLength());
                }
            }

            Serial.println("Status code: " + String(statusCode));
            //Serial.println("Response: " + response);

            if (statusCode == 200) {
                Serial.println("Event sent successfully");
            } else {
                Serial.println("Failed to send event");
            }
            
            return statusCode;
        }

        int* sendEvents(const Event* events, int n) {
            // Send events to server
            Serial.println("Sending events to server...");
            reset_last_results();

            for (int i = 0; i < n; i++){
                last_results[i] = sendEvent(events[i]);
            }

            return last_results;
        }

        int* getLastResults() {
            return last_results;
        }

        void reset_last_results() {
            for (int i = 0; i < MAX_MEASUREMENTS; i++) {
                last_results[i] = -1;
            }
        }
};

#endif // API_CLIENT_H