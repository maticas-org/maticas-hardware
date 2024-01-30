#include "Event.h"
#include "EventManager.h"
#include "Subscriber.h"
#include "Adapter.h"

class SensorsMicroService : public EventManager, public Subscriber {

    private:
        Event last_time_event_;
        vector<Event> first_measurement_event_;
        vector<Event> last_measurement_event_;
        vector<Adapter> sensors_;


    public:
        SensorsMicroService();

        //-------------------------------------------------------------
        //-------------------Event Manager Interface-------------------
        //-------------------------------------------------------------
        void main() override{
           Serial.println("\nSensorsMicroService running business logic...");
           vector<Event> events;

           //iterate over the sensors and get the data
            for (Adapter sensor : sensors_){
                Event event = sensor.request();
                events.push_back(event);
                events.push_back(event);
            }

            //update the timestamp field of the events with the last_time_event_
            for (Event event : events){
                event.setTimestamp(last_time_event_.getTimestamp());
            }

            //update the first_measurement_event_ and last_measurement_event_ fields
            first_measurement_event_ = events;
            last_measurement_event_ = events;

        }

        void notify() override{
            main();
            Serial.println("\nSensorsMicroService notifying subscribers...");

            //iterate over the subscribers and notify them
            for (Subscriber* subscriber : subscribers_){
                subscriber->notify(event);
            }
        }

        //----------------------------------------------------------
        //-------------------Subscriber Interface-------------------
        //----------------------------------------------------------
        void update(Event event) override{
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
        Event getLastMeasurementEvent() const{
            return last_measurement_event_;
        }
        void AddSensor(Adapter sensor){
            sensors_.push_back(sensor);
        }
        void RemoveSensor(Adapter sensor){
            sensors_.erase(std::remove(sensors_.begin(), sensors_.end(), sensor), sensors_.end());
        }
};
    