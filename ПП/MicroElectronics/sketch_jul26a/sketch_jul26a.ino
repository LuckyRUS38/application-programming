// Libraries
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <WiFiClientSecure.h>

// Ports
#define RELAYONE 4
#define RELAYTWO 2

const char* ssid = "Ford"; 
const char* password = "super618";
ESP8266WebServer server(80);   // Прослушиваю 80 порт
using namespace std;

void setup() {
  pinMode(RELAYONE, OUTPUT);
  pinMode(RELAYTWO, OUTPUT);
  Serial.begin(115200);
  delay(100);

  Serial.println("Connecting to ");
  Serial.println(ssid);

  // подключиться к вашей локальной wi-fi сети
  WiFi.begin(ssid, password);

  // проверить, подключился ли wi-fi модуль к wi-fi сети
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  
  Serial.println(WiFi.localIP());
  
//  Serial.begin(115200);
//  WiFi.begin(ssid, password);
//  Serial.println("");
//  Serial.print("Connecting");
//  while (WiFi.status() != WL_CONNECTED) {
//    delay(500);
//    Serial.print(".");  
//  }

  server.on("/relayModuleToggle", handleGenericArgs);  // привязать функцию обработчика к URL-пути
  server.begin();                                // запуск сервера
  Serial.println("HTTP server started");  
//  Serial.println("");
//  Serial.print("Connected to ");
//  Serial.println(ssid);
//  Serial.print("IP address: ");
//  Serial.println(WiFi.localIP());
}

void handleGenericArgs() //обработчик
{
 String message = "";

  if (server.arg("toggle")== "" && server.arg("socket")== "") 
  { // параметр не найден
    message = "Socket and Toggle Argument not found";
  }
  else
  { // параметр найден
    String toggle = server.arg("toggle");
    String socket = server.arg("socket");
    toggleRelay(socket, toggle);
    message += "toggle Argument = ";
    message += toggle;
    message += "\nsocket Argument = ";
    message += socket;
    Serial.println(message);
  }

  server.send(200, "text/plain", message);    // возвращаем HTTP-ответ
}

void toggleRelay(String numSocket, String toggle){
  if(numSocket == "1")
  {
      if(toggle == "0"){
      digitalWrite(RELAYONE, LOW);
      Serial.println("Relay off #1");  
    }
    else{
      digitalWrite(RELAYONE, HIGH);
      Serial.println("Relay on #1");  
    }
  }
  else if(numSocket == "2"){
    if(toggle == "0"){
      digitalWrite(RELAYTWO, LOW);
      Serial.println("Relay off #2");  
    }
    else{
      digitalWrite(RELAYTWO, HIGH);
      Serial.println("Relay on #2");  
    }
  }
  else{
      server.send(404, "text/plain", "NOT FOUND SOCKET");    // возвращаем HTTP-ответ
  }
}

void loop(){
  server.handleClient();
}
