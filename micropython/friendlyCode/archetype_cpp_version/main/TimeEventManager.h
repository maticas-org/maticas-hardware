#include <I2C_RTC.h>
#include "Event.h"
#include "EventManager.h"
#include "Subscriber.h"

static DS3231 RTC;

class TimeEventManager : public EventManager {
private:
    int updateIntervalSecs;

public:
    TimeEventManager(int defaultTimeUpdateIntervalSecs) {
        RTC.begin();
        //RTC.setHourMode(CLOCK_H24);
        //RTC.setDay(23);
        //RTC.setMonth(2);
        //RTC.setYear(2024);
        //RTC.setHours(16);
        //RTC.setMinutes(3);
        //RTC.setSeconds(0);

        firstEvent = Event();
        lastEvent = Event();

        updateIntervalSecs = defaultTimeUpdateIntervalSecs;

        Serial.begin(9600);
        Serial.println("Initialized TimeEventManager.");
    }

    void notify() override {
        main();

        Serial.println("\nTimeEventManager notifying subscribers...");
        for (int i = 0; i < number_of_subs; i++){
            subscribers_[i]->update(lastEvent);
        }
    }

    void main() override {
        Serial.println("\nTimeEventManager running business logic...");
        String data = "";

        try {
            String timestamp = String(RTC.getYear()) + "-" + String(RTC.getMonth()) + "-" + String(RTC.getDay()) + " " +
                               String(RTC.getHours()) + ":" + String(RTC.getMinutes()) + ":" + String(RTC.getSeconds());

            Event timeEvent(TIME_EVENT, OK_STATUS, timestamp, data);

            firstEvent = (firstEvent.getType() == UNKNOWN_EVENT) ? timeEvent : firstEvent;
            lastEvent = timeEvent;

            Serial.print("\tupdate: ");
            Serial.println(lastEvent.getTimestamp());
        } catch (const std::exception& e1) {
            Serial.print("Error on RTC read: ");
            Serial.println(e1.what());

            // Work around RTC failure
            try {
                Event timeEvent = workAroundRtcFailure();

            } catch (const std::exception& e2) {
                Serial.print("Error during work around RTC failure: ");
                Serial.println(e2.what());
            }
        }
    }

    Event workAroundRtcFailure() {
        String data = "";
        String lastTimestamp = lastEvent.getTimestamp();

        String date = lastTimestamp.substring(0, 10);
        String time = lastTimestamp.substring(11);

        int year = date.substring(0, 4).toInt();
        int month = date.substring(5, 7).toInt();
        int day = date.substring(8, 10).toInt();

        int hour = time.substring(0, 2).toInt();
        int minute = time.substring(3, 5).toInt();
        int second = time.substring(6, 8).toInt();

        second += updateIntervalSecs;
        minute += second / 60;
        second %= 60;
        hour += minute / 60;
        minute %= 60;
        day += hour / 24;
        hour %= 24;
        month += day / 30;
        day %= 30;
        year += month / 12;
        month %= 12;

        String newTimestamp = String(year) + "-" + String(month) + "-" + String(day) + " " +
                             String(hour) + ":" + String(minute) + ":" + String(second);

        Event timeEvent(TIME_EVENT, BUG_RESILIENCE_STATUS, newTimestamp, data);
        return timeEvent;
    }
};