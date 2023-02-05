import json
import os
import sys
import pyModbusTCP
import queue
import device
import mqtt
import time

debug = 0

# 192.168.9.
    # ..
    # 12 check
    # 13 check
    # 14 check
    # 15 check
    # 16 check
    # 17 check
    # 18 check
    # 19 check
    # 20 check

# Init instances
with open("config/converter.json", 'r') as f:
    json_config = json.load(f)
mqtt_host = "192.168.12.3"
mqtt_port = 1883
converter_repository = device.Converter_Repository(json_config)
measure_storage = device.Measure_Storage.stored_measures
if debug == 0:
    mqtt_client = mqtt.client
    mqtt.init(mqtt_host, mqtt_port)

def get_uspd_list(json_config):
    status_paths = []
    for i in json_config['converters']:
        for j in i['devices']:
            # status_path = f"_/Gorizont/NTE/{j['building_id']}/{j['uspd']}/status/measure"
            status_path = f"_/Gorizont/NTE/{j['uspd']}/status/measure"
            if status_path not in status_paths:
                status_paths.append(status_path)
    return status_paths

def show_devices(converter_repo_instance):
    for i in converter_repo_instance.converter_list:
        print(f"Converter: {i}")
        for j in i.devices:
            print(f"\tDevice: {j}")

def main():
    while True:
        converter_repository.receive_all()
        print("[*] Recieving done!\n")
        while measure_storage.qsize() > 0:
            meas = measure_storage.get()
            print(f"Sending measures: {meas}")
            # print(f"[*]Topic: \n{meas.get_formatted_topic_measures()}")
            # print(f"[*]Value: \n{meas.get_formatted_measures()}")
            mqtt.client.publish(
                topic=meas.get_formatted_topic_measures(), 
                payload=meas.get_formatted_measures()
                )
            mqtt.client.publish(
                topic=meas.get_formatted_topic_measures() + "_info", 
                payload=meas.get_formatted_meta_info()
                )
        for i in get_uspd_list(json_config):
            mqtt.client.publish(
                topic=i,
                payload=f"Uptime:{int(time.time())}\r\nGateway:OK\r\nChirpstack:OK"
            )
        time.sleep(60 * 15)
        
        
if __name__ == "__main__":
    print("[*] Init...")
    print("[*] Config has loaded!")
    show_devices(converter_repository)
    print("[*] Start receiving...")
    main()
    