#include "CustomUtils.h"

void logMemoryUsage() {
  long int free_hmem = ESP.getFreeHeap();
  long int total_hmem = ESP.getHeapSize();
  long int free_mem = ESP.getFreePsram();
  long int total_mem = ESP.getPsramSize();

  float usedPercentage = ((float)(total_hmem - free_hmem) * 100.0f) / (float)total_hmem;

  Serial.printf("\tFree H. memory: %d B, Total H. memory: %d B, used H. percentage: %.2f\n", free_hmem, total_hmem, usedPercentage);
  Serial.printf("\tFree memory: %d B, Total memory: %d B\n", free_mem, total_mem);
}