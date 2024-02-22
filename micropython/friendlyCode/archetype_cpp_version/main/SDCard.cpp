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
    Serial.printf("\tReading file: %s\n", path);

    File file = fs.open(path);
    if(!file){
        Serial.println("\tFailed to open file for reading");
        return;
    }

    Serial.print("\tRead from file: ");
    while(file.available()){
        Serial.write(file.read());
    }
    file.close();
}

void writeFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("\tWriting file: %s\n", path);

    File file = fs.open(path, FILE_WRITE, true);
    if(!file){
        Serial.println("\tFailed to open file for writing");
        return;
    }else{
        Serial.println("\tFile opened for writing");
    }

    if(file.print(message)){
        Serial.println("\tFile written");
    } else {
        Serial.println("\tWrite failed");
    }
    file.close();
}

bool appendFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("\tAppending to file: %s\n", path);


    File file = fs.open(path, FILE_APPEND, true);
    if(!file){
        Serial.println("\tFailed to open file for appending");
        return false;
    }else{
        Serial.println("\tFile opened for appending");
    }

    if(file.print(message)){
        Serial.println("\tMessage appended!");
        file.close();
        return true;
    } else {
        Serial.println("\tAppend failed!");
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

float getFileSize(fs::FS &fs, const char * path){
    Serial.printf("Getting file size: %s\n", path);
    File file = fs.open(path);
    if(!file){
        Serial.println("Failed to open file for reading");
        return -1.0;
    }

    float size = file.size();
    file.close();
    return size;
}

bool checkIfFileExists(fs::FS &fs, const char * path, bool createIfNotExists){
    Serial.printf("\tChecking if file exists: %s\n", path);
    if(fs.exists(path)){
        Serial.println("\tFile exists");
        return true;
    } else {
        Serial.println("\tFile does not exist");
        if (createIfNotExists) {
            Serial.println("\tCreating file...");
            File file = fs.open(path, FILE_WRITE, true);
            if (!file) {
                Serial.println("\tFailed to open file for writing");
                return false;
            }
            file.close();
            return true;
        }
        return false;
    }
}


//--------------------- DataManagementMicroService methods ---------------------
DataManagementMicroService::DataManagementMicroService() {
    Serial.println("DataManagementMicroService constructor");
    this->initSDCard();

    // initialize pending events
    for (int i = 0; i < MAX_STORED_EVENTS; i++) {
        pendingEventsToStore[i] = Event();
    }
    pendingEventsToStoreCount = 0;
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
    
    // set the name of the file to write to
    fileNumber      = 1;
    fileName = fileNameTemplate + String(fileNumber) + ".jsonl";

    // check if file exists, if not create it
    checkIfFileExists(sd, fileName.c_str(), true);

    // check if file size is greater than maximum allowed
    float fileSize = getFileSize(sd, fileName.c_str()); 

    // if file size is greater than maximum allowed, create a new file
    while (fileSize > MAX_FILE_SIZE) {
        Serial.println("\tFile size is greater than maximum allowed. Creating new file...");
        fileNumber++;
        fileName = fileNameTemplate + String(fileNumber) + ".jsonl";
        
        // check if file exists, if not create it
        checkIfFileExists(sd, fileName.c_str(), true);
        
        // check if file size is greater than maximum allowed
        fileSize = getFileSize(sd, fileName.c_str());
    }

    //check if the file exists
    if(checkIfFileExists(sd, fileName.c_str(), false)){
        Serial.println("File exists");
    }else{
        Serial.println("File does not exist");
    }
  
    Serial.println("SUCCESS - sd card initialized.");
    sd.end();
}

//--------------------- Subscriber methods ---------------------
void DataManagementMicroService::update(const Event* events, int size){
    Serial.println("DataManagementMicroService got " + String(size) + " events");
    const Event empty_event = Event();

    if (!sdCardInitialized) {
        Serial.println("SD card not initialized. Cannot write events to file.");
        return;
    }

    // if file exists, append events to it
    Serial.printf("Appending events to file %s...\n", fileName.c_str());
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
    sd.begin(CS, spi);
    delay(10);

    // append events to file if failed, store them in a circular buffer
    for (int i = 0; i < size; i++) {
        if (events[i] == empty_event) {
            continue;
        }
        Serial.println("Appending event " + String(i) + " to file " + fileName + "...");
        bool result = appendFile(sd, fileName.c_str(), events[i].toString().c_str());

        if (!result) {
            // if maximum number of events is reached, make it a circular buffer
            if (pendingEventsToStoreCount >= MAX_STORED_EVENTS) {
                pendingEventsToStoreCount = 0;
                
                if (firstTimeResetingCounter) {
                    Serial.println("Circular buffer is full. Overwriting events...");
                }else{
                    Serial.println("Circular has been full for a while. And problem persists. Rebooting...");
                    ESP.reset();
                }

                firstTimeResetingCounter = false;
            }

            pendingEventsToStore[pendingEventsToStoreCount] = events[i];
            pendingEventsToStoreCount++;
        }
    }

    // append events from circular buffer to file
    for (int i = 0; i < pendingEventsToStoreCount; i++) {
        Serial.println("Appending Pending SD Store event " + String(i) + " to file " + fileName + "...");
        bool result = appendFile(sd, fileName.c_str(), pendingEventsToStore[i].toString().c_str());

        if (result) {
            pendingEventsToStore[i] = empty_event;
        }
    }

    sd.end();
}

//--------------------- EventManager methods ---------------------
void DataManagementMicroService::notify(){

    Serial.println("DataManagementMicroService notify");

    //check if the sd card is initialized
    if (!sdCardInitialized) {
        Serial.println("\tSD card not initialized. Cannot read events from file.");
        return;
    }

    //if initialized check if the file exists and how many events are stored in it
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
    sd.begin(CS, spi);
    delay(10);

    if (!sd.exists(fileName)) {
        Serial.println("\tFile does not exist. No events to read.");
        sd.end();
    }else{
        Serial.println("\tFile exists. Reading events...");
        File file = sd.open(fileName);

        if(!file){
            Serial.println("\tFailed to open file for reading");
            sd.end();
        }else{
            //count the number of events in the file, remember that the '\n' character
            //is used to separate events
            int eventsCount = 0;

            while(file.available()){
                if(file.read() == '\n'){
                    eventsCount++;
                }
            }
            Serial.println("\tNumber of events in file: " + String(eventsCount));

            //load the events from the file to the pendingEvents array
            //reading line by line and passing each string line to the event constructor
            //to create the event object.
            //if the file is empty, do nothing
            if(eventsCount == 0){
                Serial.println("\tFile is empty. No events to read.");
                file.close();
                sd.end();
            }else{
                Serial.println("\tFile is not empty. Reading events...");
                Event pendingEventsFromSD[eventsCount];

                //if the file is not empty, read the events and store them in the
                //pendingEventsFromSD array
                file.seek(0, SeekSet);
                String eventString = "";
                int eventIndex = 0;

                while(file.available()){
                    char c = file.read();
                    if(c == '\n'){
                        Event event = Event(eventString);
                        pendingEventsFromSD[eventIndex] = event;
                        eventIndex++;
                        eventString = "";
                    }else{
                        eventString += c;
                    }
                }

                file.close();
                sd.end();

                //notify the subscribers with the events read from the file
                for (int i = 0; i < number_of_subs; i++){
                    subscribers_[i]->update(pendingEventsFromSD, eventsCount);
                }
            }
        }
    }
    sd.end();
}