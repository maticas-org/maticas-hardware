#include <vector>
#include "DHT.h"
#include "Adapter.h"
#include "Event.h"

#define DHTPIN 4 
#define DHTTYPE DHT11

DHT dht = DHT(DHTPIN, DHTTYPE);


//--------------------HELPER FUNCTIONS--------------------
float average(std::vector<float> vector) {
    float sum = 0;
    for (int i = 0; i < vector.size(); i++) {
        sum += vector[i];
    }
    return sum / vector.size();
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

    public:
        DHTAdapter(int maxRetries = 5, int retryDelay = 1000) : Adapter() {
            dht.begin();
            this->maxRetries = maxRetries;
            this->retryDelay = retryDelay;
        }
    
    Event request() override {
        Serial.println("DHTAdapter handling request...");
        return specificRequest();
    }
    
    Event specificRequest() override {
        //run specific request function if it is set
        //otherwise run default request function
        if (specificRequestFunc != nullptr) {
            return specificRequestFunc();
        } else {
            return default_request();
        }
    }
    
    Event default_request() {
        std::vector<float> temperatureVector = {};
        std::vector<float> humidityVector = {};
        
        try {
            dht.begin();
            
            for (int i = 0; i < maxRetries; i++) {
                float humidity = dht.readHumidity();
                float temperature = dht.readTemperature();
                Serial.println("Humidity: " + String(humidity) + " %\t Temperature: " + String(temperature) + " *C ");  
                
                if (isvalid(humidity) && isvalid(temperature)) {
                    temperatureVector.push_back(temperature);
                    humidityVector.push_back(humidity);
                }

                delay(retryDelay);
            }

            if (temperatureVector.size() == 0 || humidityVector.size() == 0) {
                return Event(MEASUREMENT_EVENT, INTERNAL_SERVER_ERROR, "", "No data");
            }

            float temperature = average(temperatureVector);
            float humidity = average(humidityVector);

            //format data in json like string 
            String data = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
            Event event = Event(MEASUREMENT_EVENT, OK_STATUS, "", data);
        } catch (std::exception e) {
            //print the exception, and the message
            Serial.println(e.what());

            return Event(MEASUREMENT_EVENT, INTERNAL_SERVER_ERROR, "", "DHT sensor not found");
        }
    };

 
};