#include <SoftwareSerial.h>

#define rxPin 3
#define txPin 8

// Set up a new SoftwareSerial object
SoftwareSerial mySerial =  SoftwareSerial(rxPin, txPin);

int data1 = 0;
int data2 = 0;
String inputString = "";
bool dataReceiver = false;

void Split(char* e) {
  char* v[2];
  char *p;
  int i = 0;
  p = strtok(e, ",");
  while (p && i < 2) {
    v[i] = p;
    p = strtok(NULL, ",");
    i++;
  }

  data1 = atoi(v[0]);
  data2 = atoi(v[1]);

}

void setup()  {
    Serial.begin(9600);
    // Set the baud rate for the SoftwareSerial object
    mySerial.begin(9600);
}

void loop() {
  if (mySerial.available() > 0) {
    inputString = mySerial.readStringUntil('\n'); 
    char inputCharArray[inputString.length() + 1]; 
    inputString.toCharArray(inputCharArray, inputString.length() + 1);
    Split(inputCharArray); 

    Serial.print(data1);
    Serial.print(',');
    Serial.println(data2);
  }
}
  