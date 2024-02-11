#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "Subscriber.h"
#include "Event.h"

#define SCK  18
#define MISO  19
#define MOSI  23
#define CS  5
#define MAX_STORED_EVENTS 30 //maximum number of events to store in the microservice

void listDir(fs::FS &fs, const char * dirname, uint8_t levels);
void createDir(fs::FS &fs, const char * path);
void removeDir(fs::FS &fs, const char * path);
void readFile(fs::FS &fs, const char * path);
void writeFile(fs::FS &fs, const char * path, const char * message);
bool appendFile(fs::FS &fs, const char * path, const char * message);
void renameFile(fs::FS &fs, const char * path1, const char * path2);
void deleteFile(fs::FS &fs, const char * path);

class DataManagementMicroService : public Subscriber {
  public:
    DataManagementMicroService();
    void initSDCard();
    void update(const Event* events, int size);

  private:
    bool sdCardInitialized = false;
    String fileName = "/sd/data.jsonl";
    Event pendingEvents[MAX_STORED_EVENTS]; // events to be written to the SD card
    int pendingEventsCount = 0;

    SDFS sd = SD;
    SPIClass spi = SPIClass(VSPI);
};