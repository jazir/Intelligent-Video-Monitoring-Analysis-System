# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE

ENDPOINT = "Your AWS IoT Core custom endpoint URL"
CLIENT_ID = "Jetson-Nano"
PATH_TO_CERTIFICATE = "/My-Object-Detection/JetsonNano-AWS-IoT-certs/Jetson-Nano.cert.pem"
PATH_TO_PRIVATE_KEY = "/My-Object-Detection/JetsonNano-AWS-IoT-certs/Jetson-Nano.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/My-Object-Detection/JetsonNano-AWS-IoT-certs/root-CA.crt"
TOPIC = "JetsonNano/test" # Topic to which we are sending messages. You can give any value, but make sure to update that in AWS IoT policy

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)

def connect_client():
	myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
	myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)
	myAWSIoTMQTTClient.connect()

def publish_data(msg):
	print('Begin Publish')
	message = msg
	myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
	print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)

def disconnect_client():
	print('Publish End')
	myAWSIoTMQTTClient.disconnect()

