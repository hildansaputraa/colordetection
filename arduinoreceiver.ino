#include <SoftwareSerial.h>

#define rxPin 3
#define txPin 8

// Set up a new SoftwareSerial object
SoftwareSerial mySerial =  SoftwareSerial(rxPin, txPin);

void setup()  {
    // Define pin modes for TX and RX
    
    // Set the baud rate for the SoftwareSerial object
    mySerial.begin(9600);
}

void loop() {
  if (mySerial.available()) {
    int c = mySerial.read();
    Serial.print(c); 
    }
}