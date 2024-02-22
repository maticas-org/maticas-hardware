#include "WiFi.h"
#include <ArduinoHttpClient.h>

#include "secrets.h"
#include "SDCard.h"
#include "EventManager.h"
#include "TimeEventManager.h"
#include "ConnectionEventManager.h"
#include "SensorAdapters.h"
#include "SensorsMicroService.h"


#define timeEventManagerFrequency 5
#define sensorsMicroServiceFrequency 30
#define connectionEventManagerFrequency 60*10

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
  TimeEventManager timeEventManager = TimeEventManager(timeEventManagerFrequency);
  ConnectionEventManager connectionEventManager;
  SensorsMicroService sensorsMicroService = SensorsMicroService();
  DHTAdapter dhtAdapter = DHTAdapter();
  DataManagementMicroService dataManagementMicroService = DataManagementMicroService();

  sensorsMicroService.AddSensor(&dhtAdapter);
  timeEventManager.subscribe(&sensorsMicroService);
  sensorsMicroService.subscribe(&connectionEventManager);
  connectionEventManager.subscribe(&dataManagementMicroService);
  //dataManagementMicroService.subscribe(&connectionEventManager);
  delay(100);
  
  connectionEventManager.main();
  long int free_hmem = ESP.getFreeHeap();
  long int total_hmem = ESP.getHeapSize();
  long int free_mem = ESP.getFreePsram();
  long int total_mem = ESP.getPsramSize();

  Serial.printf("Free H. memory: %d B, Total H. memory: %d B, used H. percentage: %.2f\n", free_hmem, total_hmem, ((total_hmem-free_hmem)/total_hmem)*100);
  Serial.printf("Free memory: %d B, Total memory: %d B\n", free_mem, total_mem);

  unsigned long previousTimeEventMillis = 0;
  unsigned long previousConnectionEventMillis = 0;
  unsigned long previousSensorsMicroServiceMillis = 0;
  unsigned long currentMillis = millis();

  while (true) {
    currentMillis = millis();
    
    if (currentMillis - previousTimeEventMillis >= timeEventManagerFrequency * 1000) {
      timeEventManager.notify();
      previousTimeEventMillis = currentMillis;
    }
    
    if (currentMillis - previousConnectionEventMillis >= connectionEventManagerFrequency * 1000) {
      connectionEventManager.notify();
      previousConnectionEventMillis = currentMillis;
    }

    if (currentMillis - previousSensorsMicroServiceMillis >= sensorsMicroServiceFrequency * 1000) {
      sensorsMicroService.notify();
      previousSensorsMicroServiceMillis = currentMillis;
    }

    free_hmem = ESP.getFreeHeap();
    free_mem = ESP.getFreePsram();

    Serial.printf("Free H. memory: %d B, Total H. memory: %d B, used H. percentage: %.2f\n", free_hmem, total_hmem, ((total_hmem-free_hmem)/total_hmem)*100);
    Serial.printf("Free memory: %d B, Total memory: %d B\n", free_mem, total_mem);
    delay(1000);
  }

}

