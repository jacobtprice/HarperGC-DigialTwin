# HarperGC-DigialTwin
This repository contains code and necessary certificates to establish an mqtt connection from a sensor to AWS. The first file, final-sensor-readings.ino, is an Arduino file that simply reads data from a breakbeam sensor and two DHT11 temperature/humidity sensors. This data is returned in the serial monitor. The second file, sensor_mqtt_integration.py, reads this data from the serial monitor and sends it my AWS IoT Core endpoint through an MQTT protocol.
The certs3 folder contains the private key, public key, root certificate, and device certificate that is used to connect our sensor to AWS IoT Core.
