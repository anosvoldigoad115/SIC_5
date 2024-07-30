#include <WiFi.h>
#include <HTTPClient.h>

#define TRIGPIN 33    // Trigger pin connected to the HCSR-04
#define ECHOPIN 32    // Echo pin connected to the HCSR-04
#define RED_LED 27    // Red LED pin
#define BLUE_LED 26  // Blue LED pin

// Replace with your network credentials
const char* ssid = "Anonymus";
const char* password = "bubucantik115#";

const char* serverName = "http://192.168.43.34:5000/sensor/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");

  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;
    
    long duration, distance;
    digitalWrite(TRIGPIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGPIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGPIN, LOW);
    
    duration = pulseIn(ECHOPIN, HIGH);
    distance = (duration / 2) / 29.1; // Convert to centimeters
    
    if (distance < 100) {
      digitalWrite(RED_LED, HIGH);
      digitalWrite(BLUE_LED, LOW);
    } else {
      digitalWrite(RED_LED, LOW);
      digitalWrite(BLUE_LED, HIGH);
    }

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String httpRequestData = "{\"distance\":" + String(distance) + "}";
    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(1000);  // Send a request every 1 seconds
}