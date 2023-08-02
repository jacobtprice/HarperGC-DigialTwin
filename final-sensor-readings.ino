/*
  Project Title: Sensor Readings for AWS TwinMaker Integration
  Description: This Arduino sketch will read data from 2 DHT11 sensors and a breakbeam sensor and return values to the serial monitor
  
  Authors: Jacob Price and Drake Christensen
  Date Created: July 20, 2023
  Last Modified: July 31, 2023
*/

#include "DHT.h" // DHT sensor library

// Define pins and DHT sensor type
#define LEDPIN 5 //LED pin to check if circuit is working
#define SENSORPIN 8 // breakbeam sensor
#define DHTPIN 11 // DHT11 sensor
#define DHTPIN2 3 // DHT11 sensor for computer temperature
#define DHTTYPE DHT11 

DHT dht(DHTPIN, DHTTYPE); // Create instance for first DHT sensor
DHT dht2(DHTPIN2, DHTTYPE); // Create a new instance for the second DHT sensor

// initialize breakbeam sensor
int sensorState = 0;
int lastState = 0;

void setup() {
  pinMode(SENSORPIN, INPUT);
  digitalWrite(SENSORPIN, HIGH); // turn on the pullup

  pinMode(LEDPIN, OUTPUT); // set LED pin as an output
  digitalWrite(LEDPIN, HIGH); // turn on the LED

  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));

  dht.begin(); // Begin the first DHT sensor
  dht2.begin(); // Begin the second DHT sensor
}

void loop() {
  sensorState = digitalRead(SENSORPIN);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor 1!"));
    return;
  }

  float h2 = dht2.readHumidity(); // Read humidity from the second sensor
  float t2 = dht2.readTemperature(); // Read temperature from the second sensor
  float f2 = dht2.readTemperature(true); // Read temperature as Fahrenheit from the second sensor

  // Check if any reads failed from the second sensor and exit early (to try again).
  if (isnan(h2) || isnan(t2) || isnan(f2)) {
    Serial.println(F("Failed to read from DHT sensor 2!"));
    return;
  }

  // print sensor readings as comma seperated string for python processing
  Serial.print(h);
  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.print(t2);
  Serial.print(",");
  Serial.println(sensorState);

  delay(5000); // wait 15 seconds before reading sensors again
}

