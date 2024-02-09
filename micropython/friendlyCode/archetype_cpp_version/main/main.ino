#include "secrets.h"
#include "WiFi.h"

#include "SDCard.h"
#include "EventManager.h"
#include "TimeEventManager.h"
#include "ConnectionEventManager.h"
#include "SensorAdapters.h"
#include "SensorsMicroService.h"


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  Serial.println("Hello!");
  Serial.println("Hello!");
  delay(100);
}


void loop() {
  // put your main code here, to run repeatedly:

  delay(100);

  int updateIntervalSecs = 10;
  TimeEventManager timeEventManager = TimeEventManager(updateIntervalSecs);
  ConnectionEventManager connectionEventManager;
  SensorsMicroService sensorsMicroService = SensorsMicroService();
  DHTAdapter dhtAdapter = DHTAdapter();
  DataManagementMicroService dataManagementMicroService = DataManagementMicroService();

  sensorsMicroService.AddSensor(&dhtAdapter);
  timeEventManager.subscribe(&sensorsMicroService);
  sensorsMicroService.subscribe(&dataManagementMicroService);
  delay(100);
  
  connectionEventManager.main();

  while (true) {
    timeEventManager.notify();
    delay(updateIntervalSecs * 1000);
    connectionEventManager.notify();
    delay(updateIntervalSecs * 1000);
    sensorsMicroService.notify();
  }

}

