#include "DHT.h"
#include <TM1637.h>

#define DHTPIN D2
#define DHTTYPE DHT11   // DHT 11
#define CLK D3
#define DIO D4\

TM1637 tm(CLK,DIO);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  tm.set(7);
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);
  int humidity = dht.readHumidity() * 100;
  int temperature = dht.readTemperature() * 100;
  
  tm.display(0, 10);
  tm.display(1, 10);
  tm.display(2, 10);
  tm.display(3, 10);
  delay(1000);
  tm.display(0, t / 1000 % 10);
  tm.display(1, t / 100 % 10);
  tm.point(2);
  tm.display(2, t / 10 % 10);
  tm.display(3, t % 10);
  delay(5000);
  tm.display(0, 11);
  tm.display(1, 11);
  tm.display(2, 11);
  tm.display(3, 11);
  delay(1000);
  tm.display(0, h / 1000 % 10);
  tm.display(1, h / 100 % 10);
  tm.point(2);
  tm.display(2, h / 10 % 10);
  tm.display(3, h % 10);
  delay(5000);
}
