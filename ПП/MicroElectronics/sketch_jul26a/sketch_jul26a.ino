#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

#define PIR D0

const char* ssid = "Ford";
const char* password =  "super618";
const String url = "http://192.168.239.224/relayModuleToggle";
bool lamp = false;

void setup(){
  pinMode(PIR,INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
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

void loop(){
  if(digitalRead(PIR) == HIGH){
    if(!lamp){
      send_data("1", "1");
      lamp = true;
      Serial.println("ON");
    }
  }
  else{
    if(lamp){
      lamp = false;
      send_data("1", "0");
      Serial.println("OFF");
    }
  }
  delay(500);
}

void send_data(String device, String to_do){
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    String data = "?socket=" + device + "&toggle=" + to_do;
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
}
