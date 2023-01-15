import paho.mqtt.client

client = paho.mqtt.client.Client()


def init(host, port = 1883):
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port)
    client.publish("DEBUG/Connected", 1)
    client.on_disconnect = on_disconnect
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[*] Server: {host} connected.")
    else:
        raise ConnectionError("!!! Server is unavailable !!")
    #TODO: Implement
    pass

def on_message(client, userdata, msg):
    pass

def on_disconnect(client, userdata, flags, rc):
    print("[*] Mqtt_disconnected!")
    client.publish("DEBUG/Connected", 0)
