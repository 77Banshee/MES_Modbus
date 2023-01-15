import json
import os
import sys
import pyModbusTCP
import queue
import device
import mqtt

#192.168.9.
    #..
    #..
    #13
    #14
    #15
    #16
    #..
    #..
    #19
    #20

# Init variables
with open("config/converter.json", 'r') as f:
    json_config = json.load(f)

# Init instances
converter_repository = device.Converter_Repository(json_config)
measure_storage = device.Measure_Storage.stored_measures
mqtt_client =  mqtt.client
mqtt.init("192.168.12.3")

def show_devices(converter_repo_instance):
    for i in converter_repository.converter_list:
        print(f"Converter: {i}")
        for j in i.devices:
            print(f"\tDevice: {j}")

if __name__ == "__main__":
    print("[*] Init...")
    print("[*] Config has loaded!")
    show_devices(converter_repository)
    print("[*] Start receiving...")
    
    while True:
        converter_repository.receive_all()
        print("[*] Recieving done!\n")