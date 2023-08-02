#%%
'''
    Project Title: Sensor Data Integration to AWS IoT Core with MQTT Protocol
    Description: This Python script reads data from the serial monitor (sent from Arduino IDE), processes and packages this information, and sends it directly to AWS IoT Core using the 
                 MQTT protocol. Note that this Python script requires several configuration settings that are listed below. Visual Studio Code IDE was used to run this script.
    Requirements: This script requires boto3, json, serial, time, and psutil libraries. In addition, the associated AWS account must be configured using the awscli library. The Root CA1 
                  certificate, device certificate, and private key must all be accessible in the working environment. To run the script without a Python IDE, run "python {script_name}.py"
                  in the computer terminal and press enter. Ensure the path is specified as well.

    Authors: Jacob Price and Drake Christensen
    Date Created: July 20, 2023
    Last Modified: Jul 31, 2023
'''

#%% imports
import boto3
import json
import serial
import time
import psutil

#%% Broker / certifcation configuration
# AWS IoT Core endpoint
mqtt_broker_endpoint = "a4gwbsni06dqq-ats.iot.us-east-1.amazonaws.com"

# Thing's certificate files; ensure file path is correct
root_ca_path = 'certs3/AmazonRootCA1.pem'
cert_path = 'certs3/device-cert.pem.crt'
key_path = 'certs3/private.pem.key'

# The topic to which the message is published, change if applicable
topic = "arduino/temphumid"

#%% sending messages
# Reads data from serial monitor; change port as necessary
arduino = serial.Serial("COM3", 9600, timeout=1)

# Initializing temperature/humidity values
temperature_old = 0
temperature = 0     # office temperature
humidity = 0
temperature_old2 = 0
temperature2 = 0        # computer temperature
desk_state1 = 0

# function for reading CPU utilization percentage
def get_cpu_utilization():
    return psutil.cpu_percent(interval=0.1)

while True:
    # strip data from serial monitor and seperate into variables
    # Read all available data in the serial buffer
    data_bytes = arduino.read_all()
    # Convert the bytes to a string
    data_str = data_bytes.decode()
    # Split the data into lines
    lines = data_str.splitlines()

    # Use the last line (most recent line)
    if len(lines) > 0:
        data = lines[-1].strip()
    else:
        # If no data is available, skip this iteration
        continue
    if data:
        vals = data.split(',')
        if len(vals) == 4:
            humidity = float(vals[0]) # in percent
            temperature_old = float(vals[1]) # in degrees celsius
            temperature_old2 = float(vals[2]) # in degrees celsius
            desk_state1 = float(vals[3]) # desk occupied or not
    cpu_utilization = get_cpu_utilization() # percent cpu percentage

    # convert to degrees fahrenheit
    temperature = (temperature_old * 9/5) + 32
    temperature2 = (temperature_old2 *9/5) + 32

    # convert sensor reading into statement
    if desk_state1 == 1:
        occupant = "Desk Unoccupied"
    if desk_state1 == 0:
        occupant = "Desk Occupied"

    # Print the data
    print("Temp: {:.1f} F    Humidity: {}%      Computer Temperature: {}    Desk State: {}      CPU Utilization: {}%".format(temperature, humidity, temperature2, occupant, cpu_utilization))

    # configure message statement
    message = {
        'temperature': temperature,
        'computertemperature': temperature2,
        'humidity': humidity,
        'desk': occupant,
        'cpu': cpu_utilization
    }

    # Create an AWS IoT Core client
    iot_client = boto3.client('iot-data', region_name='us-east-1')

    # Load the certificates and key
    with open(root_ca_path, 'r') as root_ca_file:
        root_ca = root_ca_file.read()

    with open(cert_path, 'r') as cert_file:
        certificate = cert_file.read()

    with open(key_path, 'r') as key_file:
        private_key = key_file.read()

    # Publish the message to the topic
    response = iot_client.publish(
        topic=topic,
        qos=1,  # Using QoS level 1
        payload=json.dumps(message)
    )

    # Check the response status to see if the message was published successfully
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Message published successfully.")
    else:
        print("Failed to publish the message.")

    # Wait for 15 seconds before the next update
    time.sleep(2)
