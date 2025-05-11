#include <SoftwareSerial.h>

SoftwareSerial sdsSerial(4, 3);

byte buffer[10];

void setup() {
  Serial.begin(9600);
  sdsSerial.begin(9600);
}

void loop() {
  if (sdsSerial.available() >= 10) {
    if (sdsSerial.read() == 0xAA) {
      if (sdsSerial.read() == 0xC0) {
        buffer[0] = 0xAA;
        buffer[1] = 0xC0;
        
        for (int i = 2; i < 10; i++) {
          buffer[i] = sdsSerial.read();
        }

        int pm25 = buffer[2] + buffer[3] * 256;
        int pm10 = buffer[4] + buffer[5] * 256;

        float pm25f = pm25 / 10.0;
        float pm10f = pm10 / 10.0;

        Serial.print("PM2.5: ");
        Serial.print(pm25f);
        Serial.print(" µg/m³ | PM10: ");
        Serial.print(pm10f);
        Serial.println(" µg/m³");
      }
    }
  }
}
