#ifndef SDCard_h
#define SDCard_h

#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "Event.h"
#include "Subscriber.h"
#include "EventManager.h"

#define SCK  18
#define MISO  19
#define MOSI  23
#define CS  5
#define MAX_STORED_EVENTS 30 //maximum number of events to store in the microservice
#define MAX_FILE_SIZE 1024 //maximum file size in bytes
#define MAX_MEMORY_USAGE_PERCENTAGE 90 //maximum memory usage percentage

void listDir(fs::FS &fs, const char * dirname, uint8_t levels);
void createDir(fs::FS &fs, const char * path);
void removeDir(fs::FS &fs, const char * path);
void readFile(fs::FS &fs, const char * path);
void writeFile(fs::FS &fs, const char * path, const char * message);
bool appendFile(fs::FS &fs, const char * path, const char * message);
void renameFile(fs::FS &fs, const char * path1, const char * path2);
void deleteFile(fs::FS &fs, const char * path);

class DataManagementMicroService : public Subscriber, public EventManager {
  public:
    DataManagementMicroService();
    void initSDCard();
    String defaultSetFileName();
    void update(const Event* events, int size);
    void notify() override;

  private:
    bool sdCardInitialized = false;
    String fileNameTemplate = "/sd/data";
    String fileName = "";
    int fileNumber = 1;

    Event pendingEventsToStore[MAX_STORED_EVENTS]; // events to be written to the SD card
    int pendingEventsToStoreCount = 0;
    bool firstTimeResetingCounter = true;

    SDFS sd = SD;
    SPIClass spi = SPIClass(VSPI);
};

#endif