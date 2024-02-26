#include "SDCard.h"
File file;


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

    File afile = root.openNextFile();
    while(afile){
        if(afile.isDirectory()){
            Serial.print("  DIR : ");
            Serial.print (afile.name());
            time_t t= afile.getLastWrite();
            struct tm * tmstruct = localtime(&t);
            Serial.printf("  LAST WRITE: %d-%02d-%02d %02d:%02d:%02d\n",(tmstruct->tm_year)+1900,( tmstruct->tm_mon)+1, tmstruct->tm_mday,tmstruct->tm_hour , tmstruct->tm_min, tmstruct->tm_sec);
            if(levels){
                listDir(fs, afile.path(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(afile.name());
            Serial.print("  SIZE: ");
            Serial.print(afile.size());
            time_t t= afile.getLastWrite();
            struct tm * tmstruct = localtime(&t);
            Serial.printf("  LAST WRITE: %d-%02d-%02d %02d:%02d:%02d\n",(tmstruct->tm_year)+1900,( tmstruct->tm_mon)+1, tmstruct->tm_mday,tmstruct->tm_hour , tmstruct->tm_min, tmstruct->tm_sec);
        }
        afile = root.openNextFile();
    }
}

/*
* This method is used to get the file with the smallest last write time (this is the oldest file, 
* the one that has been written the first) or the file with the greatest last write time (this is the
* newest file, the one that has been written the last). This can be controlled by the max parameter.
*
* - max = false: get the oldest file, the one with the smallest last write time.
* - max = true: get the newest file, the one with the greatest last write time.
*/
String getPriorityFileName(fs::FS &fs, const char * dirname, bool max = false) {
    File root = fs.open(dirname);

    if(!root){
        Serial.println("Failed to open directory");
        return "";
    }

    if(!root.isDirectory()){
        Serial.println("Not a directory");
        return "";
    }

    //sort them by the last write 
    //and return the smallest one
    File afile = root.openNextFile();

    if (!max){
        time_t minTime = afile.getLastWrite();
        String minFileName = afile.name();

        while(afile){
            if(afile.isDirectory()){
                afile = root.openNextFile();
                continue;
            }

            time_t t= afile.getLastWrite();
            if (t < minTime) {
                minTime = t;
                minFileName = afile.name();
            }
            afile = root.openNextFile();
        }

        return minFileName;
    }else{
        time_t maxTime = afile.getLastWrite();
        String maxFileName = afile.name();

        while(afile){
            if(afile.isDirectory()){
                afile = root.openNextFile();
                continue;
            }

            time_t t= afile.getLastWrite();
            if (t > maxTime) {
                maxTime = t;
                maxFileName = afile.name();
            }
            afile = root.openNextFile();
        }

        return maxFileName;
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

    file = fs.open(path);
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

    file = fs.open(path, FILE_WRITE, true);
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
    file = fs.open(path, FILE_APPEND, true);

    if(!file){
        Serial.println("\tFailed to open file for appending");
        return false;
    }else{
        Serial.println("\tFile opened for appending");
    }

    if(file.print(message)){
        Serial.println("\tMessage appended!");
        float fileSize = file.size();
        Serial.printf("\tFile size: %f\n", fileSize);
        file.close();
        return true;
    } else {
        Serial.println("\tAppend failed!");
        float fileSize = file.size();
        Serial.printf("\tFile size: %f\n", fileSize);
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
    file = fs.open(path);
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
            file = fs.open(path, FILE_WRITE, true);
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

/*
* This method is used to get the default file name for the data management microservice.
* If the file is not set then it generates a new file name based on the template and the file number.
* If the memory is at the maximum usage percentage then it deletes the oldest file and creates a new one.
* If the file size is greater than the maximum allowed then it creates a new file, and if the next new file
* already existed, it checks if its smaller than the maximum allowed size, if not it continues creating new files
* until it finds one that is smaller than the maximum allowed size.
*/
String DataManagementMicroService::defaultSetFileName() {

   if (fileName == "") {
        fileName = fileNameTemplate + String(fileNumber) + ".jsonl";
    }

    // initialize SPI
    spi.begin(SCK, MISO, MOSI, CS);
    delay(50);
    sd.begin(CS, spi);
    delay(50);

    // check sd card memory usage
    float totalMemory = sd.cardSize();
    float usedMemory = sd.usedBytes();
    float memoryUsagePercentage = (usedMemory / totalMemory) * 100;
    Serial.printf("Memory usage percentage: %f\n", memoryUsagePercentage);

    // if memory usage is greater than maximum allowed, delete oldest file
    if (memoryUsagePercentage > MAX_MEMORY_USAGE_PERCENTAGE) {
        Serial.println("Memory usage is greater than maximum allowed. Deleting oldest file...");
        String priorityFileName = getPriorityFileName(sd, "/sd");
        deleteFile(sd, priorityFileName.c_str());
    }

    // check if file exists, if not create it
    checkIfFileExists(sd, fileName.c_str(), true);

    // check if file size is greater than maximum allowed
    float fileSize = getFileSize(sd, fileName.c_str()); 

    // if file size is greater than maximum allowed, create a new file
    while (fileSize > MAX_FILE_SIZE) {
        Serial.println("File size is greater than maximum allowed. Creating new file...");
        fileNumber++;
        fileName = fileNameTemplate + String(fileNumber) + ".jsonl";
        
        // check if file exists, if not create it
        checkIfFileExists(sd, fileName.c_str(), true);
        
        // check if file size is greater than maximum allowed
        fileSize = getFileSize(sd, fileName.c_str());
    }

    return fileName; 
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
    defaultSetFileName();

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

    // append events to file.
    // if failed, store them in a circular buffer
    for (int i = 0; i < size; i++) {
        if (events[i] == empty_event) {
            continue;
        }

        // set the name of the file to write to
        defaultSetFileName();

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
                    ESP.restart();
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

    //get the name of the file with the smallest last write time
    String priorityFileName = "/sd/" + getPriorityFileName(sd, "/sd");
    Serial.println("Priority file to notify: " + priorityFileName);

    if (!sd.exists(priorityFileName)) {
        Serial.println("\tFile does not exist. No events to read.");
        sd.end();
    }else{
        Serial.println("\tFile exists. Reading events...");
        File file = sd.open(priorityFileName);

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
                //delete the file
                deleteFile(sd, priorityFileName.c_str());
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