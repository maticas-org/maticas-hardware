#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "Subscriber.h"

#define SCK  18
#define MISO  19
#define MOSI  23
#define CS  5

void initSDCard();
void listDir(fs::FS &fs, const char * dirname, uint8_t levels);
void createDir(fs::FS &fs, const char * path);
void removeDir(fs::FS &fs, const char * path);
void readFile(fs::FS &fs, const char * path);
void writeFile(fs::FS &fs, const char * path, const char * message);
void appendFile(fs::FS &fs, const char * path, const char * message);
void renameFile(fs::FS &fs, const char * path1, const char * path2);
void deleteFile(fs::FS &fs, const char * path);

class DataManagementMicroService : public Subscriber {
  public:
    DataManagementMicroService();
    void update(const Event* events, int size);

  private:
    String fileName = "/data.jsonl";
};