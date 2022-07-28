#include "DHT.h"
#include <TM1637.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

#define DHTPIN D2
#define DHTTYPE DHT11   // DHT 11
#define CLK D3
#define DIO D4

const char* ssid = "Ford";
const char* password = "super618";
//String url = "http://192.168.239.166:5000/weather?&id=B";
String url = "http://narodmon.ru/get?ID=84:CC:A8:B3:37:51";
TM1637 tm(CLK,DIO);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  tm.set(7);
  dht.begin();
  Serial.println("");
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void display_data(int t, int h){
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

void send_data(int temperature, int humidity){
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    String data = "&temp2=" + String(temperature / 100) + "&humid2=" + String(humidity / 100);
    String fullUrl = url + data;
    Serial.println("Requesting " + fullUrl);
    if (http.begin(client, fullUrl)) {
      int httpCode = http.GET();
      Serial.println("============== Response code: " + String(httpCode));
      if (httpCode > 0) {
        Serial.println(http.getString());
      }
      http.end();
    } else {
      Serial.printf("[HTTP] Unable to connect\n");
    }
  }
  delay(5000);
}

int timer = 300000;

void loop() {
  int humidity = dht.readHumidity() * 100;
  int temperature = dht.readTemperature() * 100;
  display_data(temperature, humidity);
  if (timer > 300000){
    send_data(temperature, humidity);
    timer = 0;
  }
  timer += 12000;
}
