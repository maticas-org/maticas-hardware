#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "SDCard.h"


void listDir(fs::FS &fs, const char * dirname, uint8_t levels){
    Serial.printf("Listing directory: %s\n", dirname);

    File root = fs.open(dirname);
    if(!root){
        Serial.println("Failed to open directory");
        return;
    }
    if(!root.isDirectory()){
        Serial.println("Not a directory");
        return;
    }

    File file = root.openNextFile();
    while(file){
        if(file.isDirectory()){
            Serial.print("  DIR : ");
            Serial.print (file.name());
            time_t t= file.getLastWrite();
            struct tm * tmstruct = localtime(&t);
            Serial.printf("  LAST WRITE: %d-%02d-%02d %02d:%02d:%02d\n",(tmstruct->tm_year)+1900,( tmstruct->tm_mon)+1, tmstruct->tm_mday,tmstruct->tm_hour , tmstruct->tm_min, tmstruct->tm_sec);
            if(levels){
                listDir(fs, file.path(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(file.name());
            Serial.print("  SIZE: ");
            Serial.print(file.size());
            time_t t= file.getLastWrite();
            struct tm * tmstruct = localtime(&t);
            Serial.printf("  LAST WRITE: %d-%02d-%02d %02d:%02d:%02d\n",(tmstruct->tm_year)+1900,( tmstruct->tm_mon)+1, tmstruct->tm_mday,tmstruct->tm_hour , tmstruct->tm_min, tmstruct->tm_sec);
        }
        file = root.openNextFile();
    }
}

void createDir(fs::FS &fs, const char * path){
    Serial.printf("Creating Dir: %s\n", path);
    if(fs.mkdir(path)){
        Serial.println("Dir created");
    } else {
        Serial.println("mkdir failed");
    }
}

void removeDir(fs::FS &fs, const char * path){
    Serial.printf("Removing Dir: %s\n", path);
    if(fs.rmdir(path)){
        Serial.println("Dir removed");
    } else {
        Serial.println("rmdir failed");
    }
}

void readFile(fs::FS &fs, const char * path){
    Serial.printf("Reading file: %s\n", path);

    File file = fs.open(path);
    if(!file){
        Serial.println("Failed to open file for reading");
        return;
    }

    Serial.print("Read from file: ");
    while(file.available()){
        Serial.write(file.read());
    }
    file.close();
}

void writeFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Writing file: %s\n", path);

    File file = fs.open(path, FILE_WRITE, true);
    if(!file){
        Serial.println("Failed to open file for writing");
        return;
    }else{
        Serial.println("File opened for writing");
    }

    if(file.print(message)){
        Serial.println("File written");
    } else {
        Serial.println("Write failed");
    }
    file.close();
}

bool appendFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Appending to file: %s\n", path);


    File file = fs.open(path, FILE_APPEND, true);
    if(!file){
        Serial.println("Failed to open file for appending");
        return false;
    }else{
        Serial.println("File opened for appending");
    }

    if(file.print(message)){
        Serial.println("Message appended");
        file.close();
        return true;
    } else {
        Serial.println("Append failed");
        file.close();
        return false;
    }
}

void renameFile(fs::FS &fs, const char * path1, const char * path2){
    Serial.printf("Renaming file %s to %s\n", path1, path2);
    if (fs.rename(path1, path2)) {
        Serial.println("File renamed");
    } else {
        Serial.println("Rename failed");
    }
}

void deleteFile(fs::FS &fs, const char * path){
    Serial.printf("Deleting file: %s\n", path);
    if(fs.remove(path)){
        Serial.println("File deleted");
    } else {
        Serial.println("Delete failed");
    }
}

void DataManagementMicroService::initSDCard() {
    Serial.println("Initializing sd card...");

    // initialize SPI
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
  
    // initialize sd card
    if (!sd.begin(CS, spi)) {
        Serial.println("Card Mount Failed");
        sdCardInitialized = false;
        return;
    }else{
        Serial.printf("sd card mounted successfully with %lluMB\n", (sd.cardSize()/1024)/1000000);
        Serial.printf("sd card type: sd%s\n", sd.cardType() == CARD_MMC ? "MMC" : "HC");
        Serial.printf("Used MBs: %llu\n", (sd.usedBytes()/1024)/1000);
    }

    sdCardInitialized = true;

    if (sd.exists(fileName)) {
        Serial.printf("File %s exists\n", fileName.c_str());
    } else {
        Serial.printf("File %s does not exist, creating...\n", fileName.c_str());

        File file = sd.open(fileName, FILE_WRITE, true);
        if (!file) {
        Serial.println("Failed to open file for writing");
        return;
        }
        file.close();
    }
  
    Serial.println("SUCCESS - sd card initialized.");
    sd.end();
}

DataManagementMicroService::DataManagementMicroService() {
    Serial.println("DataManagementMicroService constructor");
    this->initSDCard();

    // initialize pending events
    for (int i = 0; i < MAX_STORED_EVENTS; i++) {
        pendingEvents[i] = Event();
    }
    pendingEventsCount = 0;
}

void DataManagementMicroService::update(const Event* events, int size){
    Serial.println("DataManagementMicroService got " + String(size) + " events");
    const Event empty_event = Event();

    if (!sdCardInitialized) {
        Serial.println("SD card not initialized. Cannot write events to file.");
        return;
    }

    // if file exists, append events to it
    Serial.println("File exists. Appending events...");
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
    sd.begin(CS, spi);

    // append events to file if failed, store them in a circular buffer
    for (int i = 0; i < size; i++) {
        if (events[i] == empty_event) {
            continue;
        }
        Serial.println("Appending event " + String(i) + " to file...");
        bool result = appendFile(sd, fileName.c_str(), events[i].toString().c_str());

        if (!result) {
            // if maximum number of events is reached, make it a circular buffer
            if (pendingEventsCount >= MAX_STORED_EVENTS) {
                pendingEventsCount = 0;
            }

            pendingEvents[pendingEventsCount] = events[i];
            pendingEventsCount++;
        }
    }

    // append events from circular buffer to file
    for (int i = 0; i < pendingEventsCount; i++) {
        Serial.println("Appending pending event " + String(i) + " to file...");
        bool result = appendFile(sd, fileName.c_str(), pendingEvents[i].toString().c_str());

        if (result) {
            pendingEvents[i] = empty_event;
        }
    }

    sd.end();
}

