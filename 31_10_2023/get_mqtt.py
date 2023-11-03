import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code: " + str(rc))
    client.subscribe("get_all_data")
    client.subscribe("get_node_data")
    client.subscribe("get_master_data")
    client.subscribe("get_gateway_data")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Received message on topic '{topic}': {payload}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="truc", password="1234")
client.connect("192.168.1.107", 1883, 60)

client.loop_forever()