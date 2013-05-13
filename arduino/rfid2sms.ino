// RFID2SMS
// Read RFID from SL018/030, send the ID as an SMS using SM5100B.
// Circuit:
//   * Standard SM5100B shield from SparkFun
//   * SL030 -> Arduino:
//     - VCC -> 3V3
//     - SDA -> A4
//     - SCL -> A5
//     - OUT -> A3
//     - GND -> GND

#define DEBUG 1

#include <Wire.h>
#include <SL018.h>
#include <SoftwareSerial.h>
#include <string.h>
#include <QueueArray.h>


#ifdef DEBUG
#define console(s) Serial.print("DEBUG: "); Serial.println(s);
#else
#define console(s) ;
#endif /* DEBUG */


SoftwareSerial cell(2, 3);
SL018 rfid;

// TAG pin (low level when tag present)
#define TAG 17 // A3
#define checkTagPresent() !digitalRead(TAG)
#define checkCell() while (cell.available()) { Serial.write(cell.read()); } delay(1000);


boolean tagRead = false;
boolean modemReady = true;
QueueArray <char *> rfidQueue;


void setup() {
  pinMode(TAG, INPUT);
  Wire.begin();
  Serial.begin(9600);
  cell.begin(9600);
}


void loop() {
  if (tagRead && !checkTagPresent()) {
    tagRead = false;
    return;
  }

  if (!tagRead && checkTagPresent()) {
    rfid.seekTag();
    if (!checkTagPresent()) return;
    while(!rfid.available());
    console("Tag present:"); console(rfid.getTagString());
    {
      char *tagString = (char *)calloc(sizeof(char), 14);
      memcpy(tagString, rfid.getTagString(), 14);
      rfidQueue.push(tagString);
    }
    tagRead = true;
  }
  
  while (cell.available()) { Serial.write(cell.read()); }

  if (!rfidQueue.isEmpty() && modemReady) {
    char *rfid = rfidQueue.pop();
    console("Sending RFID via SMS.");
    checkCell();
    cell.println("AT+CMGF=1");
    checkCell();
    console("Setting address.");
    cell.println("AT+CMGS=\"+442033225814\"");
    checkCell();
    console("Writing body");
    cell.println(rfid);
    checkCell();
    console("Writing escape");
    cell.write('\x1A');
    checkCell();
    delay(1000);
  }
}

