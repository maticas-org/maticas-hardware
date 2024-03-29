#include "DHT.h"
#include "Adapter.h"
#include "Event.h"
#include "secrets.h"

#define DHTPIN 4
#define DHTTYPE DHT11
#define MAX_RETRIES 5

DHT dht = DHT(DHTPIN, DHTTYPE);

//--------------------HELPER FUNCTIONS--------------------
float average(float values[], int size) {
    if (size == 0) {
        return 0;
    }

    float sum = 0;
    for (int i = 0; i < size; i++) {
        sum += values[i];
    }
    return sum / size;
}

bool isvalid(float value) {
    return !isnan(value) && !isinf(value) && value > 0;
}

//--------------------ADAPTERS--------------------
class DHTAdapter : public Adapter {
private:
    Event (*specificRequestFunc)() = nullptr;
    int maxRetries;
    int retryDelay;
    long int lastRequestTimestamp = -1;

public:
    DHTAdapter(int maxRetries = 5, int retryDelay = 2100) : Adapter() {
        dht.begin();
        this->maxRetries = maxRetries;
        this->retryDelay = retryDelay;
    }

    Event request(Event timeEvent){
        Serial.println("DHTAdapter handling request...");
        return specificRequest(timeEvent);
    }

    Event specificRequest(Event timeEvent){
        // Run specific request function if it is set
        // Otherwise, run the default request function
        if (specificRequestFunc != nullptr) {
            return specificRequestFunc();
        } else {
            return default_request(timeEvent);
        }
    }

    Event default_request(Event timeEvent) {
        float temperatureArray[maxRetries];
        float humidityArray[maxRetries];

        try {
            dht.begin();
            int validReadings = 0;

            for (int i = 0; i < maxRetries; i++) {
                float humidity = dht.readHumidity();
                float temperature = dht.readTemperature();
                Serial.println("Humidity: " + String(humidity) + " %\t Temperature: " + String(temperature) + " *C ");

                if (isvalid(humidity) && isvalid(temperature)) {
                    temperatureArray[i] = temperature;
                    humidityArray[i] = humidity;
                    validReadings++;
                }

                delay(retryDelay);
            }

            if (validReadings == 0) {
                Serial.println("No valid data.");
                return Event(MEASUREMENT_EVENT, INTERNAL_SERVER_ERROR, "", "No valid data");
            }

            float temperature = average(temperatureArray, validReadings);
            float humidity = average(humidityArray, validReadings);

            // Format data in JSON-like string as a list of measurements
            const String timestamp = String(timeEvent.getTimestamp());
            const String data1 = "{\"variable\": " + TEMPERATURE_UIID + ", \"value\": " + String(temperature) + ", \"crop\": " + CROP_UIID + ", \"timestamp\": \"" + timestamp + "\"}";
            const String data2 = "{\"variable\": " + HUMIDITY_UIID + ", \"value\": " + String(humidity) + ", \"crop\": " + CROP_UIID + ", \"timestamp\": \"" + timestamp + "\"}";
            const String data = "[" + data1 + ", " + data2 + "]";
            return Event(MEASUREMENT_EVENT, OK_STATUS, timestamp, data);

        } catch (std::exception e) {
            // Print the exception and the message
            Serial.println(e.what());
            return Event(MEASUREMENT_EVENT, INTERNAL_SERVER_ERROR, "", "DHT sensor not found");
        }
    }
};
