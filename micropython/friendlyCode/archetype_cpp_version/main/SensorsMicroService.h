#include "Event.h"
#include "EventManager.h"
#include "Subscriber.h"
#include "Adapter.h"

#define MAX_STORED_EVENTS 30 //maximum number of events to store in the microservice
#define MAX_SENSORS 10 //maximum number of sensors to store in the microservice

class SensorsMicroService : public EventManager, public Subscriber {

    private:
        Event last_time_event_;
        Event first_measurement_event_;
        Event last_measurement_events_[MAX_STORED_EVENTS];
        Adapter* sensors_[MAX_SENSORS];
        int last_measurement_index_; // Index to keep track of the last stored measurement event
        int sensors_count;

        Subscriber* subscribers_[MAX_NUMBER_OF_SUBSCRIBERS];
        int number_of_subs;

    public:
        SensorsMicroService(){
            sensors_count = 0;
            last_measurement_index_ = 0;
            number_of_subs = 0;

            // Initialize last_measurement_events_ to empty events
            for (int i = 0; i < MAX_STORED_EVENTS; i++) {
                last_measurement_events_[i] = Event();
            }
        }

        //-------------------------------------------------------------
        //-------------------Event Manager Interface-------------------
        //-------------------------------------------------------------
        void main() override {
            Serial.println("\nSensorsMicroService running business logic...");

            // Iterate over the sensors and get the data
            for (int i = 0; i < MAX_SENSORS; i++) {
                if (i < sensors_count && sensors_[i] != nullptr) {
                    Event event = sensors_[i]->request();
                    last_measurement_index_ = (last_measurement_index_ + 1) % MAX_STORED_EVENTS; // Update index
                    last_measurement_events_[last_measurement_index_] = event; // Store event

                    // Update the timestamp field of the event with the last_time_event_
                    last_measurement_events_[last_measurement_index_].setTimestamp(last_time_event_.getTimestamp());
                    Serial.println("SensorsMicroService got event: ");
                    Serial.print(last_measurement_events_[last_measurement_index_].toString());
                }
            }

            // Update the first_measurement_event_ and last_measurement_event_ fields
            first_measurement_event_ = last_measurement_events_[(last_measurement_index_ + 1) % MAX_STORED_EVENTS];
        }


        void notify() override{
            main();
            Serial.println("\nSensorsMicroService notifying subscribers...");

            //iterate over the subscribers and notify them
            for (int i = 0; i < number_of_subs; i++){
                subscribers_[i]->update(last_measurement_events_, MAX_STORED_EVENTS); 
            }
        }

        void subscribe(Subscriber* subscriber){
            Serial.println("\nSensorsMicroService subscribing...");
            if (number_of_subs < MAX_NUMBER_OF_SUBSCRIBERS){
                subscribers_[number_of_subs] = subscriber;
                number_of_subs++;
            }else{
                Serial.println("Max number of subscribers reached.");
            }
        }

        void unsubscribe(Subscriber* subscriber){
            Serial.println("\nSensorsMicroService unsubscribing...");   
            for (int i = 0; i < number_of_subs; i++){
                if (subscribers_[i] == subscriber){
                    for (int j = i; j < number_of_subs - 1; j++){
                        subscribers_[j] = subscribers_[j + 1];
                    }
                    number_of_subs--;
                    break;
                }
            }
        }

        //----------------------------------------------------------
        //-------------------Subscriber Interface-------------------
        //----------------------------------------------------------
        void update(const Event& event) override {
            Serial.println("\nSensorsMicroService got event: ");
            Serial.print(event.toString());

            if (event.getType() == TIME_EVENT){
                last_time_event_ = event;
                notify();
            }else{
                Serial.println("\nSensorsMicroService got an event of type: ");
                Serial.print(event.getType());
                Serial.println("Which is unsuporrted by this microservice");
            }
        }
        
        
        //----------------------------------------------------
        //-------------------Business Logic-------------------
        //----------------------------------------------------
        Event getFirstMeasurementEvent() const{
            return first_measurement_event_;
        }
        const Event* getLastMeasurementEvent() const{
            return last_measurement_events_;
        }
        void AddSensor(Adapter* sensor) {
            if (sensors_count < MAX_SENSORS) {
                sensors_[sensors_count] = sensor; // Add sensor pointer to the array
                sensors_count++; // Increment the count of added sensors
            } else {
                Serial.println("Max number of sensors reached.");
            }
        }

        void RemoveSensor(Adapter* sensor) {
            // Find and remove the sensor
            for (int i = 0; i < sensors_count; i++) {
                if (sensors_[i] == sensor) {
                    for (int j = i; j < sensors_count - 1; j++) {
                        sensors_[j] = sensors_[j + 1]; // Shift sensors to fill the gap
                    }
                    sensors_count--; // Decrement the count of added sensors
                    break;
                }
            }
        }

};
    