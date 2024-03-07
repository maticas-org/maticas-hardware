#include "SDCard.h"
#include "CustomUtils.h"

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
        afile.close();
        afile = root.openNextFile();
    }
    root.close();
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
    }else{
        Serial.printf("Root file/dir opened: %s\n", dirname);
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
            logMemoryUsage();
            Serial.printf("File: %s\n", afile.name());

            if(afile.isDirectory()){
                afile = root.openNextFile();
                continue;
            }

            time_t t= afile.getLastWrite();
            if (t < minTime) {
                minTime = t;
                minFileName = afile.name();
            }
            afile.close();
            afile = root.openNextFile();
        }
        root.close();
        return minFileName;
    }else{
        time_t maxTime = afile.getLastWrite();
        String maxFileName = afile.name();

        while(afile){
            logMemoryUsage();
            Serial.printf("File: %s\n", afile.name());

            if(afile.isDirectory()){
                afile = root.openNextFile();
                continue;
            }

            time_t t= afile.getLastWrite();
            if (t > maxTime) {
                maxTime = t;
                maxFileName = afile.name();
            }
            afile.close();
            afile = root.openNextFile();
        }
        root.close();
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
        file.close();
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
        file.close();
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
        file.close();
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

    // check sd card memory usage
    float totalMemory = sd.cardSize();
    float usedMemory = sd.usedBytes();
    float memoryUsagePercentage = (usedMemory*100.0)/totalMemory;
    Serial.printf("SD Card usage percentage: %f\n", memoryUsagePercentage);

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



void DataManagementMicroService::writeEventsBatch() {
    if (!sdCardInitialized || pendingEventsToStoreCount == 0) {
        return; // Nothing to write or SD card not initialized
    }

    Serial.printf("Writing batch of %d events to file %s...\n", pendingEventsToStoreCount, fileName.c_str());
    File file = sd.open(fileName.c_str(), FILE_APPEND, true);

    if (!file) {
        Serial.println("Failed to open file for batch append");
        return;
    }else{
        Serial.println("File opened for batch append");
    }
    
    for (int i = 0; i < pendingEventsToStoreCount; ++i) {
        Serial.printf("Writing event %d to file... ", i);

        //ommit events that are not measurement events
        if (pendingEventsToStore[i].getType() != MEASUREMENT_EVENT){
            Serial.println("Event is not a measurement event. Skipping...");
            continue;
        }

        String eventData = pendingEventsToStore[i].toString(); // Assuming Event has a toJson method
        if (!file.println(eventData)) { // Use println to ensure each event is on a new line
            Serial.println("Failed to write event to file");
        }else{
            Serial.println("OK");
        }
    }

    file.close();
    pendingEventsToStoreCount = 0; // Reset the count after writing
    Serial.println("Batch write complete.");
}

EventArray DataManagementMicroService::getEventsFromSDDynamic(){

    Serial.println("DataManagementMicroService extracting data from SD card...");
    EventArray events = EventArray(MAX_STORED_EVENTS);

    //check if the sd card is initialized
    if (!sdCardInitialized) {
        Serial.println("\tSD card not initialized. Cannot read events from file.");
        return events;
    }

    //if initialized check if the file exists and how many events are stored in it
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
    bool started_ok = sd.begin(CS, spi);
    delay(100);

    if (!started_ok) {
        Serial.println("\tFailed to start SD card");
        sd.end();
        return events;
    }

    //get the name of the file with the smallest last write time
    String priorityFileName = "/sd/" + getPriorityFileName(sd, "/sd");
    Serial.println("Priority file to notify: " + priorityFileName);
    logMemoryUsage();

    if (!sd.exists(priorityFileName)) {
        Serial.println("\tFile does not exist. No events to read.");
        sd.end();
        return events;
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

            //fix the events count to the minimum between the number of events in the file
            //and the maximum number of events that can be stored MAX_STORED_EVENTS
            eventsCount = min(eventsCount, MAX_STORED_EVENTS);

            //load the events from the file to the pendingEvents array
            //reading line by line and passing each string line to the event constructor
            //to create the event object.
            //if the file is empty, do nothing
            if(eventsCount == 0){
                Serial.println("\tFile is empty. No events to read.");
                file.close();
                sd.end();
                return events;
            }else{
                Serial.println("\tFile is not empty. Reading events...");

                //if the file is not empty, read the events and store them in the
                //pendingEventsFromSD array
                file.seek(0, SeekSet);
                String eventString = "";
                int eventIndex = 0;

                while(file.available()){
                    char c = file.read();
                    if(c == '\n'){
                        Event event = Event(eventString);
                        events[eventIndex] = event;
                        eventIndex++;
                        eventString = "";
                    }else{
                        eventString += c;
                    }
                }

                file.close();
                //delete the file
                logMemoryUsage();
                deleteFile(sd, priorityFileName.c_str());
                sd.end();
                logMemoryUsage();
            
                return events;
            }
        }
    }
    sd.end();
}

//--------------------- Subscriber methods ---------------------
void DataManagementMicroService::update(const Event* events, int size) {
    Serial.printf("DataManagementMicroService received %d events\n", size);
    logMemoryUsage();

    if (!sdCardInitialized) {
        Serial.println("SD card not initialized. Cannot write events to file.");
        return;
    }

    //if initialized check if the file exists and how many events are stored in it
    spi.begin(SCK, MISO, MOSI, CS);
    delay(100);
    sd.begin(CS, spi);
    delay(10);

    // Set/Update the name of the file to write to
    int threshold = max(MAX_STORED_EVENTS, EVENT_BATCH_SIZE);

    // If the buffer is full or will be full after adding the new events, make sure to set to a new file
    // or to an existing file with enough space
    if (pendingEventsToStoreCount >= threshold || pendingEventsToStoreCount + size >= threshold) {
        defaultSetFileName();
    }

    logMemoryUsage();

    for (int i = 0; i < size; ++i) {
        // Attempt to write the batch to SD card if the buffer is full
        if (pendingEventsToStoreCount >= MAX_STORED_EVENTS) {
            defaultSetFileName();
            writeEventsBatch(); // Attempt to write current batch before overwriting old events
        }

        // Insert the new event into the buffer, possibly overwriting the oldest event
        int insertPosition = pendingEventsToStoreCount % MAX_STORED_EVENTS;
        pendingEventsToStore[insertPosition] = events[i];

        if (pendingEventsToStoreCount < MAX_STORED_EVENTS) {
            // Only increment count if we haven't filled the buffer yet
            pendingEventsToStoreCount++;
        }

        // Attempt to write after each insert if we've reached the batch size
        // This check is outside the condition to ensure we attempt to write as soon as possible
        if (pendingEventsToStoreCount >= EVENT_BATCH_SIZE) {
            defaultSetFileName();
            writeEventsBatch(); // If we've reached batch size, write the batch
        }
    }
    sd.end();
}


