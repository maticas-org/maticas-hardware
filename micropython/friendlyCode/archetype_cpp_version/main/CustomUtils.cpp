#include "CustomUtils.h"

void logMemoryUsage() {
  long int free_hmem = ESP.getFreeHeap();
  long int total_hmem = ESP.getHeapSize();
  long int free_mem = ESP.getFreePsram();
  long int total_mem = ESP.getPsramSize();

  Serial.printf("\tFree H. memory: %d B, Total H. memory: %d B, used H. percentage: %.2f\n", free_hmem, total_hmem, ((total_hmem-free_hmem)/total_hmem)*100);
  Serial.printf("\tFree memory: %d B, Total memory: %d B\n", free_mem, total_mem);
}