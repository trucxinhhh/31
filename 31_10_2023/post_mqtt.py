import paho.mqtt.client as mqtt
import json
from time import sleep
from random import randint
from datetime import datetime
num = 1

mqtt_connected = False


def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    print("Connected with Result Code: " + str(rc))
    mqtt_connected = True
    client.publish("status",json.dumps({"status": "Connected"}))

def on_disconnect(client, userdata, rc): 
    global mqtt_connected
    print("Disconnected From Broker")
    client.publish("status",0)
    mqtt_connected = False
    


def update_master_data( led1_status, led2_status,temp, humi):
    data = {
            "led1_status": led1_status,
            "led2_status": led2_status,
            "temp": temp,
            "humi": humi
        }   
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_master_data", json_data)

def update_gateway_data(lamp, siren):
    data = {
        "lamp": lamp,
        "siren": siren
    } 
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_gateway_data", json_data)


def update_node_data(vibration, relay, Light_Sensor, Distance_Sensor):
    data = {
        "vibration": vibration,
        "relay": relay,
        "Light_Sensor": Light_Sensor,
        "Distance_Sensor": Distance_Sensor
    }  
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_node_data", json_data)


def update_all_data(led1_status, led2_status,temp, humi, lamp, siren,vibration, relay, Light_Sensor, Distance_Sensor):
    data = {
            "led1_status": led1_status,
            "led2_status": led2_status,
            "temp": temp,
            "humi": humi,
            "lamp": lamp,
            "siren": siren,
            "vibration": vibration,
            "relay": relay,
            "Light_Sensor": Light_Sensor,
            "Distance_Sensor": Distance_Sensor
    } 
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_all_data", json_data)



client = mqtt.Client('D02')
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.username_pw_set(username="truc", password="1234")
client.connect("192.168.1.57", 1883, 60)
while True:
    client.loop()
    humi = float(randint(70,100))
    temp = float(randint(20,30))
    time=str(datetime.now().isoformat())
    # _id=num
    led1=randint(0,1)
    led2=randint(0,1)
    lamp=randint(0,1)
    siren=randint(0,1)
    vibration=randint(0,1)
    relay=randint(0,1)
    Light_Sensor=randint(20,40)
    Distance_Sensor=randint(0,500)
    update_master_data(led1,led2,temp,humi)
    update_gateway_data(lamp,siren)
    update_node_data(vibration,relay,Light_Sensor,Distance_Sensor)
    update_all_data(led1,led2,temp, humi,lamp,siren,vibration,relay,Light_Sensor,Distance_Sensor)

    num+=1
    sleep(3)
