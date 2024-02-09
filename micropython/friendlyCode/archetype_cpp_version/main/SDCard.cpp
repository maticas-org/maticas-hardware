#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "SDCard.h"


void initSDCard() {
  Serial.println("Initializing SD card...");

  // initialize SPI
  SPIClass spi = SPIClass(VSPI);
  spi.begin(SCK, MISO, MOSI, CS);
  delay(100);
  
  // initialize SD card
  if (!SD.begin(CS, spi)) {
    Serial.println("Card Mount Failed");
    return;
  }
  
  Serial.println("SUCCESS - SD card initialized.");
}

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

    File file = fs.open(path, FILE_WRITE);
    if(!file){
        Serial.println("Failed to open file for writing");
        return;
    }
    if(file.print(message)){
        Serial.println("File written");
    } else {
        Serial.println("Write failed");
    }
    file.close();
}

void appendFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Appending to file: %s\n", path);

    File file = fs.open(path, FILE_APPEND);
    if(!file){
        Serial.println("Failed to open file for appending");
        return;
    }
    if(file.print(message)){
        Serial.println("Message appended");
    } else {
        Serial.println("Append failed");
    }
    file.close();
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


DataManagementMicroService::DataManagementMicroService() {
    initSDCard();
    Serial.println("DataManagementMicroService constructor");
}

void DataManagementMicroService::update(const Event* events, int size){
    Serial.println("DataManagementMicroService got " + String(size) + " events");
    const Event empty_event = Event();

    if (!SD.exists(fileName)) {
        Serial.println("File does not exist. Creating file...");
        writeFile(SD, fileName.c_str(), "{}");
    } else {
        Serial.println("File exists. Appending events...");
        for (int i = 0; i < size; i++) {
            if (events[i] == empty_event) {
                continue;
            }
            Serial.println("Appending event " + String(i) + " to file...");
            appendFile(SD, fileName.c_str(), events[i].toString().c_str());
        }
    }
}

//void DataManagementMicroService::update(const Event events[], int size){
//    Serial.println("DataManagementMicroService got" + String(size) + "events" );
//    const Event empty_event = Event();
//
//    if (!SD.exists(fileName)) {
//        Serial.println("File does not exist. Creating file...");
//        writeFile(SD, fileName.c_str(), "{}");
//    } else {
//        for (int i = 0; i < size; i++) {
//
//            if (events[i] == empty_event) {
//                continue;
//            }
//            Serial.println("Appending event" + String(i) + " to file...");
//            appendFile(SD, fileName.c_str(), events[i].toString().c_str());
//        }
//    }
//}