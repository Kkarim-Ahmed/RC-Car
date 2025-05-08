#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

int A1 = 12;
int A2 = 14;
int B1 = 27;
int B2 = 26;

AsyncWebServer server(80);
unsigned long lastCmd = 0;

void setup() {
  Serial.begin(115200);
  
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(B1, OUTPUT);
  pinMode(B2, OUTPUT);
  stopCar();

  WiFi.softAP("Deeeza's Iphone", "12341234");
  Serial.println(WiFi.softAPIP());

  server.on("/cmd", HTTP_GET, [](AsyncWebServerRequest *r){
    String c = r->getParam("c")->value();
    lastCmd = millis();
    
    if(c == "f") forward();
    else if(c == "b") backward();
    else if(c == "l") left();
    else if(c == "r") right();
    else stopCar();
    
    r->send(200, "text/plain", "ok");
  });

  server.begin();
}

void loop() {
  if(millis() - lastCmd > 1000) stopCar();
}

void forward() {
  digitalWrite(A1, HIGH);
  digitalWrite(A2, LOW);
  digitalWrite(B1, HIGH);
  digitalWrite(B2, LOW);
}

void backward() {
  digitalWrite(A1, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(B1, LOW);
  digitalWrite(B2, HIGH);
}

void left() {
  digitalWrite(A1, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(B1, HIGH);
  digitalWrite(B2, LOW);
}

void right() {
  digitalWrite(A1, HIGH);
  digitalWrite(A2, LOW);
  digitalWrite(B1, LOW);
  digitalWrite(B2, HIGH);
}

void stopCar() {
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(B1, LOW);
  digitalWrite(B2, LOW);
}