#include "secrets.h"
#include "WiFi.h"

#include "EventManager.h"
#include "TimeEventManager.h"
#include "ConnectionEventManager.h"
#include "SensorAdapters.h"
#include "SensorsMicroService.h"


//void initSDCard();

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  //void initSDCard();

  Serial.println("Hello!");
  Serial.println("Hello!");
  delay(100);
}


void loop() {
  // put your main code here, to run repeatedly:

  int updateIntervalSecs = 10;
  TimeEventManager timeEventManager = TimeEventManager(updateIntervalSecs);
  ConnectionEventManager connectionEventManager;
  SensorsMicroService sensorsMicroService = SensorsMicroService();
  DHTAdapter dhtAdapter = DHTAdapter();
  delay(100);
  
  connectionEventManager.main();

  while (true) {
    timeEventManager.main();
    delay(updateIntervalSecs * 1000);
    connectionEventManager.main();
    delay(updateIntervalSecs * 1000);
    Event ans =  dhtAdapter.request();

    Serial.println(ans.toString());
  }

}


/*
*
*
*
*
*
*
*/

//void initSDCard() {
//  Serial.println("Initializing SD card...");
//
//  // initialize SPI
//  SPIClass spi = SPIClass(VSPI);
//  spi.begin(SCK, MISO, MOSI, CS);
//  delay(100);
//  
//  // initialize SD card
//  if (!SD.begin(CS, spi)) {
//    Serial.println("Card Mount Failed");
//    return;
//  }
//  
//  Serial.println("SUCCESS - SD card initialized.");
//}
//