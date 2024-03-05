#!/bin/bash

# Identify the Arduino serial port
SERIAL_PATH="/dev/ttyUSB0"
echo "Arduino device found on $SERIAL_PATH"

# Set the baud rate (modify this according to your needs)
BAUD_RATE=9600
stty -F $SERIAL_PATH $BAUD_RATE

# Start capturing serial output (in the background)
cat $SERIAL_PATH > output.txt &
CAT_PID=$!
echo "Started capturing serial output to output.txt (PID: $CAT_PID)"

# Periodically display the last part of output.txt
# Adjust '-n 20' to change the number of lines displayed
# Adjust '-n 2' to change the update interval
watch -d -n 2 tail -n 20 output.txt

# Cleanup: Stop the background `cat` command when the script is stopped
cleanup() {
    echo "Stopping capture..."
    kill $CAT_PID
    stty -F $SERIAL_PATH -hupcl
    echo "Capture stopped."
}
trap cleanup EXIT
