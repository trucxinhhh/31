import requests
import json
from datetime import datetime
from random import randint
from time import sleep
import paho.mqtt.client as mqtt
import threading

client = mqtt.Client()
# Hàm xử lý khi nhận được thông điệp từ broker MQTT
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")

# Hàm để subscribe MQTT
def subscribe_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("192.168.1.107", 1883, 60)  # Thay mqtt_broker_ip bằng địa chỉ IP của MQTT broker
    client.subscribe("get_master_data")
    client.loop_forever()

# Hàm để thực hiện HTTP POST
def http_post():
    while True:
        current_time = datetime.now()
        timestamp = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(timestamp)

        data_master = {
            "id": 1,
            "led1_status": 1,
            "led2_status": 1,
            "temp": randint(20, 30),
            "humi": randint(70, 90),
            "timestamp": timestamp
        }

        json_data_master = json.dumps(data_master)
        api_key = "lBJGSf9VWp9g5ok"
        api_url_master = 'http://192.168.1.107:8000/update_master_data'
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": api_key
        }

        response_master = requests.post(api_url_master, data=json_data_master, headers=headers)

        if response_master.status_code == 200:
            print("Dữ liệu Master đã được cập nhật thành công.")
            client.publish("get_master_data", "activate_subscribe")
        else:
            print("Có lỗi xảy ra khi cập nhật dữ liệu Master:", response_master.status_code, response_master.text)
        
        sleep(5)

# Bắt đầu luồng MQTT subscribe và luồng HTTP POST
mqtt_thread = threading.Thread(target=subscribe_mqtt)
http_thread = threading.Thread(target=http_post)

mqtt_thread.start()
http_thread.start()
