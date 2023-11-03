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
    


def update_master_data(id, led1_status, led2_status,temp, humi, timestamp):
    data = {
            "id": id,
            "led1_status": led1_status,
            "led2_status": led2_status,
            "temp": temp,
            "humi": humi,
            "timestamp": str(timestamp)
        }   
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_master_data", json_data)

def update_gateway_data(id, lamp, siren, timestamp):
    data = {
        "id": id,
        "lamp": lamp,
        "siren": siren,
        "timestamp": str(timestamp)
    } 
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_gateway_data", json_data)


def update_node_data(id, vibration, relay, Light_Sensor, Distance_Sensor, timestamp):
    data = {
        "id": id,
        "vibration": vibration,
        "relay": relay,
        "Light_Sensor": Light_Sensor,
        "Distance_Sensor": Distance_Sensor,
        "timestamp": timestamp
    }  
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_node_data", json_data)


def update_all_data(id,led1_status, led2_status,temp, humi, lamp, siren,vibration, relay, Light_Sensor, Distance_Sensor, timestamp):
    data = {
            "id" : id,
            "led1_status": led1_status,
            "led2_status": led2_status,
            "temp": temp,
            "humi": humi,
            "lamp": lamp,
            "siren": siren,
            "vibration": vibration,
            "relay": relay,
            "Light_Sensor": Light_Sensor,
            "Distance_Sensor": Distance_Sensor,
            "timestamp": timestamp
    } 
    json_data = json.dumps(data)
    print(json_data)
    client.publish("update_all_data", json_data)

# def create_json(data1, data2, data4):
#     data = {
#         "id": int(data1),  # id
#         "data": int(data2),
#         "timestamp": str(data4)  
#     }
#     json_data = json.dumps(data)
#     return json_data


# def send_single_data_json(data1, data2, data3, data4, data5, data6,data7): 
#     client.publish("temp_json", create_json(data1,data2,data3,data4))
#     client.publish("humi_json", create_json(data1,data2,data3,data5))
#     client.publish("led1_json", create_json(data1,data2,data3,data6))
#     client.publish("led2_json", create_json(data1,data2,data3,data7))
#     client.subscribe("post_all_data_json")



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
    _id=num
    led1=randint(0,1)
    led2=randint(0,1)
    lamp=randint(0,1)
    siren=randint(0,1)
    vibration=randint(0,1)
    relay=randint(0,1)
    Light_Sensor=randint(20,40)
    Distance_Sensor=randint(0,500)
    update_master_data(_id,led1,led2,temp,humi,time)
    update_gateway_data(_id,lamp,siren,time)
    update_node_data(_id,vibration,relay,Light_Sensor,Distance_Sensor,time)
    update_all_data(_id,led1,led2,temp, humi,lamp,siren,vibration,relay,Light_Sensor,Distance_Sensor,time)

    num+=1
    sleep(3)
