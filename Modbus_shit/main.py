import json
import os
import sys
import pyModbusTCP
import queue
import device
import mqtt

debug = 1

#192.168.9.
    #..
    #..
    #13 check
    #14 check
    #15 check
    #16 
    #..
    #..
    #19 check
    #20 check

# Init instances
with open("config/converter.json", 'r') as f:
    json_config = json.load(f)
mqtt_host = "192.168.12.3"
mqtt_port = 1883
converter_repository = device.Converter_Repository(json_config)
measure_storage = device.Measure_Storage.stored_measures
if debug == 0:
    mqtt_client =  mqtt.client
    mqtt.init(mqtt_host, mqtt_port)

def show_devices(converter_repo_instance):
    for i in converter_repo_instance.converter_list:
        print(f"Converter: {i}")
        for j in i.devices:
            print(f"\tDevice: {j}")

def main():
    converter_repository.receive_all()
    print("[*] Recieving done!\n")

if __name__ == "__main__":
    print("[*] Init...")
    print("[*] Config has loaded!")
    show_devices(converter_repository)
    print("[*] Start receiving...")
    main()
    print("[*] Queue: ")
    while measure_storage.qsize() > 0:
        meas = measure_storage.get()
        print(meas)