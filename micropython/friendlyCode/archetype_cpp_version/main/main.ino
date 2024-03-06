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
#define timeEventManagerFrequency 5               //5 seconds
#define sensorsMicroServiceFrequency 5*1         //2 minutes
#define connectionEventManagerFrequency 30*1     //10 minutes
#define dataManagementMicroServiceFrequency 60*1  //11 minutes
#define LED 2

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  Serial.println("Hello!");
  Serial.println("Hello!");
  pinMode(LED,OUTPUT);
  digitalWrite(LED,LOW);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

  delay(100);
  TimeEventManager timeEventManager = TimeEventManager(timeEventManagerFrequency);
  ConnectionEventManager connectionEventManager;
  SensorsMicroService sensorsMicroService = SensorsMicroService();
  DHTAdapter dhtAdapter = DHTAdapter();
  DataManagementMicroService dataManagementMicroService = DataManagementMicroService();

  sensorsMicroService.AddSensor(&dhtAdapter);
  timeEventManager.subscribe(&sensorsMicroService);
  sensorsMicroService.subscribe(&connectionEventManager);
  connectionEventManager.subscribe(&dataManagementMicroService);
  dataManagementMicroService.subscribe(&connectionEventManager);
  delay(100);
  
  connectionEventManager.main();
  logMemoryUsage();

  unsigned long previousTimeEventMillis = 0;
  unsigned long previousConnectionEventMillis = 0;
  unsigned long previousSensorsMicroServiceMillis = 0;
  unsigned long previousDataManagementMicroServiceMillis = 0;
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

    //update the data management - this tries to send the data from the sd card to the server
    if (currentMillis - previousDataManagementMicroServiceMillis >= dataManagementMicroServiceFrequency * 1000) {
      Serial.println("\n------------------------\n");
      dataManagementMicroService.notify();
      previousDataManagementMicroServiceMillis = currentMillis;
    }

    //show memory usage
    logMemoryUsage();
    delay(2500);
  }

}

