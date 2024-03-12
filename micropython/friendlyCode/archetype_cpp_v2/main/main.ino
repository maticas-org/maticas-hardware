#include "WiFi.h"
#include <ArduinoHttpClient.h>

#include "CustomUtils.h"
#include "secrets.h"
#include "SDCard.h"
#include "EventManager.h"
#include "TimeEventManager.h"
#include "ConnectionEventManager.h"
#include "SensorAdapters.h"
#include "SensorsMicroService.h"


//time in seconds
#define timeEventManagerFrequency 5              //5 seconds
#define sensorsMicroServiceFrequency 40*1        //2 minutes
#define connectionEventManagerFrequency 41*1    //10 minutes
#define sdStoreFrequency 60*2                    //11 minutes
#define sdLoadFrequency 60*1                     //12 minutes
#define LED 2

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  Serial.println("Hello!");
  Serial.println("Hello!");
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  delay(1000);
}

void loop() {

  delay(100);
  TimeEventManager timeEventManager = TimeEventManager(timeEventManagerFrequency);
  ConnectionEventManager connectionEventManager;
  SensorsMicroService sensorsMicroService = SensorsMicroService();
  DHTAdapter dhtAdapter = DHTAdapter();
  DataManagementMicroService dataManagementMicroService = DataManagementMicroService();


  sensorsMicroService.AddSensor(&dhtAdapter);
  timeEventManager.subscribe(&sensorsMicroService);
  sensorsMicroService.subscribe(&connectionEventManager);
  delay(100);
  logMemoryUsage();
  connectionEventManager.main();
  logMemoryUsage();

  unsigned long previousTimeEventMillis = 0;
  unsigned long previousConnectionEventMillis = 0;
  unsigned long previousSensorsMicroServiceMillis = 0;
  unsigned long sdStoreMillis = 0;
  unsigned long sdLoadMillis = 0;
  unsigned long currentMillis = millis();

  while (true) {
    currentMillis = millis();
    
    //update the time
    if (currentMillis - previousTimeEventMillis >= timeEventManagerFrequency * 1000) {
      timeEventManager.notify();
      previousTimeEventMillis = currentMillis;
    }
    currentMillis = millis();
    
    //update the connection
    if (currentMillis - previousConnectionEventMillis >= connectionEventManagerFrequency * 1000) {
      connectionEventManager.notify();
      previousConnectionEventMillis = currentMillis;
    }
    currentMillis = millis();

    //update the time
    if (currentMillis - previousTimeEventMillis >= timeEventManagerFrequency * 1000) {
      timeEventManager.notify();
      previousTimeEventMillis = currentMillis;
    }
    currentMillis = millis();

    //update the measurements from sensors
    if (currentMillis - previousSensorsMicroServiceMillis >= sensorsMicroServiceFrequency * 1000) {
      sensorsMicroService.notify();
      previousSensorsMicroServiceMillis = currentMillis;
    }
    currentMillis = millis();

    //update the time
    if (currentMillis - previousTimeEventMillis >= timeEventManagerFrequency * 1000) {
      timeEventManager.notify();
      previousTimeEventMillis = currentMillis;
    }
    currentMillis = millis();

    //update the data management - this tries to store the data in the sd card
    if (currentMillis - sdStoreMillis >= sdStoreFrequency * 1000) {
      Serial.println("Storing data in the SD card ************************************");
      Serial.println("Storing data in the SD card ************************************");
      dataManagementMicroService.update(connectionEventManager.measurementEvents, connectionEventManager.measurementEventsCount);
      connectionEventManager.flushEvents();
      sdStoreMillis = currentMillis;
    }

    //update the time
    if (currentMillis - previousTimeEventMillis >= timeEventManagerFrequency * 1000) {
      timeEventManager.notify();
      previousTimeEventMillis = currentMillis;
    }
    currentMillis = millis();

    //load the data from the sd card - this tries to send the data from the sd card to the server
    if (currentMillis - sdLoadMillis >= sdLoadFrequency * 1000) {
      Serial.println("Loading data from the SD card ------------------------------------");
      Serial.println("Loading data from the SD card ------------------------------------");
      //send the pending data to the server
      connectionEventManager.sendPendingData(); 
      //get the events from the sd card
      EventArray events = dataManagementMicroService.getEventsFromSDDynamic(); 
      //update the connection event manager with the events from the sd card, so 
      //they can be sent to the server
      connectionEventManager.updateFromLoadedEvents(events);
      sdLoadMillis = currentMillis;
    }

    //show memory usage
    logMemoryUsage();
    delay(2500);
  }

}

