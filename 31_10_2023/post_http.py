import requests
import json
from datetime import datetime
from random import randint
from time import sleep
import paho.mqtt.client as mqtt
# Lấy thời gian hiện tại
current_time = datetime.now()
timestamp = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))

# Dữ liệu bạn muốn gửi lên các API POST
data_master = {
    "id": 1,
    "led1_status": 1,
    "led2_status": 1,
    "temp": randint(20,30),
    "humi": randint(70,90),
    "timestamp": timestamp
}

data_gateway = {
    "id": 1,
    "lamp": 1,
    "siren": 1,
    "timestamp": timestamp
}

data_node = {
    "id": 1,
    "vibration": 1,
    "relay": 1,
    "Light_Sensor": randint(100,500),
    "Distance_Sensor": randint(0,100),
    "timestamp": timestamp
}

data_button = {
        "id" : 0,
        "led1_status":1 ,
        "led2_status":1 ,
        "temp": 40,
        "humi": 60,
        "lamp": 1,
        "siren": 0,
        "vibration": 1,
        "relay":1 ,
        "Light_Sensor":450 ,
        "Distance_Sensor":4 ,
        "timestamp": timestamp
}

# Chuyển đổi dữ liệu thành định dạng JSON
json_data_master = json.dumps(data_master)
json_data_gateway = json.dumps(data_gateway)
json_data_node = json.dumps(data_node)
json_data_button = json.dumps(data_button)

# URL của các API POST bạn muốn gửi dữ liệu lên
API_KEY='lBJGSf9VWp9g5ok'
api_url_master = 'http://192.168.1.107:8000/update_master_data'
api_url_gateway = 'http://192.168.1.107:8000/update_gateway_data'
api_url_node = 'http://192.168.1.107:8000/update_node_data'
api_url_button = 'http://192.168.1.107:8000/update_all_data'

api_key = "lBJGSf9VWp9g5ok"

# Gửi yêu cầu POST với dữ liệu JSON và API Key cho từng API
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": api_key
}
while True:
    current_time = datetime.now()
    timestamp = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    print(timestamp)
    response_master = requests.post(api_url_master, data=json_data_master, headers=headers)
    response_gateway = requests.post(api_url_gateway, data=json_data_gateway, headers=headers)
    response_node = requests.post(api_url_node, data=json_data_node, headers=headers)
    response_button = requests.post(api_url_button, data=json_data_button, headers=headers)
    client.loop()
    # Kiểm tra kết quả
    if response_master.status_code == 200:
        print("Dữ liệu Master đã được cập nhật thành công.")
        
        
    else:
        print("Có lỗi xảy ra khi cập nhật dữ liệu Master:", response_master.status_code, response_master.text)

    if response_gateway.status_code == 200:
        print("Dữ liệu Gateway đã được cập nhật thành công.")
    else:
        print("Có lỗi xảy ra khi cập nhật dữ liệu Gateway:", response_gateway.status_code, response_gateway.text)

    if response_node.status_code == 200:
        print("Dữ liệu Node đã được cập nhật thành công.")
    else:
        print("Có lỗi xảy ra khi cập nhật dữ liệu Node:", response_node.status_code, response_node.text)

    if response_button.status_code == 200:
        print("Dữ liệu các Button đã được cập nhật thành công.")
    else:
        print("Có lỗi xảy ra khi cập nhật dữ liệu Button:", response_button.status_code, response_button.text)
    sleep(5)
