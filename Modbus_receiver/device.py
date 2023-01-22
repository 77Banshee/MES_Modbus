from pyModbusTCP.client import ModbusClient
import struct
import json
import time
import queue

class Measure_Storage(object):
    stored_measures = queue.Queue()

class Collected_Measures(object):
    def __init__(self, device_instance, measures) -> None:
        self.measures = measures
        self.device_instance = device_instance
    def get_formatted_measures(self):
        if self.device_instance.type == "ZET_7054_Inclinometer":
            return f"{int(time.time())}\r\n{self.measures[0]}\r\n{self.measures[1]}"
        elif self.device_instance.type == "ZET_Thermometer":
            formatted_measures = ""
            formatted_measures += f"{int(time.time())}\r\n"
            formatted_measures += f"{self.device_instance.quantity}\r\n"
            for i in self.measures:
                formatted_measures += f"{i}\r\n"
            return formatted_measures
        elif self.device_instance.type == "ZET_Accelerometer":
            return f"{int(time.time())}\r\n{self.measures[0]}\r\n{self.measures[1]}\r\n{self.measures[2]}"
        elif self.device_instance.type == "ZET_Hygrometer":
            humidity = int(self.measures[0])
            temperature = round(self.measures[1], 1)
            pressure = round(self.measures[2],2)
            return f"{int(time.time())}\r\n{humidity}\r\n{pressure}\r\n{temperature}"
    def get_formatted_topic_measures(self):
        if self.device_instance.type == "ZET_7054_Inclinometer":
            return f"_/Gorizont/{self.device_instance.object_id}/{self.device_instance.building_id}/{self.device_instance.uspd}/Inclinometer/{self.device_instance.building_id}_{self.device_instance.name}/from_device/measure"
        elif self.device_instance.type == "ZET_Thermometer":
            return f"_/Gorizont/{self.device_instance.object_id}/{self.device_instance.building_id}/{self.device_instance.uspd}/Thermometer/{self.device_instance.building_id}_{self.device_instance.name}/from_device/measure"
        elif self.device_instance.type == "ZET_Accelerometer":
            return f"_/Gorizont/{self.device_instance.object_id}/{self.device_instance.building_id}/{self.device_instance.uspd}/Accelerometer/{self.device_instance.building_id}_{self.device_instance.name}/from_device/measure"
        elif self.device_instance.type == "ZET_Hygrometer":
            return f"_/Gorizont/{self.device_instance.object_id}/{self.device_instance.building_id}/{self.device_instance.uspd}/Hygrometer/{self.device_instance.building_id}_{self.device_instance.name}/from_device/measure"
            
    def __str__(self) -> str:
        return f"{self.device_instance.type} {self.device_instance.name} {self.device_instance.id} {self.measures}"

class Converter_Repository(object):
    def __init__(self, json_config: str):
        self.converter_list = []
        self.json_config = json_config
        self.init_converter_list()

    def init_converter_list(self):
        converter_list_raw = self.json_config["converters"]
        for i in range(0, len(converter_list_raw)):
            # print(f"[*] Init converter {converter_list_raw[i]['name']}")
            self.converter_list.append(
                Zet7076_Converter(
                    ip_address=converter_list_raw[i]['ip_address'],
                    name=converter_list_raw[i]['name'],
                    sensor_list_raw=converter_list_raw[i]['devices']
                )
            )
    def receive_all(self):
        for i in self.converter_list:
            print(f"Request converter: {i.ip_address} {i.name}...")
            i.request_data()

class Zet7076_Converter(object):
    def __init__(self, ip_address: str, name: str, sensor_list_raw, port: int=502):
        self.ip_address = ip_address
        self.name = name
        self.port = port
        self.devices = []
        self.init_devices(sensor_list_raw)
        print()

    def __str__(self):
        return f"Zet_Converter: Name: {self.name}, ip_address: {self.ip_address}"

    def init_devices(self, sensor_list_raw):
        for i in sensor_list_raw:
            print(i['name'])
            if i['type'] == 'ZET_7054_Inclinometer':
                    self.devices.append(
                        Zet_Inclinometer(
                            id=i["id"],
                            type=i["type"],
                            name=i["name"],
                            slave=i['slave'],
                            x_low_high_regs=i['registers']['x'], 
                            y_low_high_regs=i['registers']['y'],
                            object_id=i["object_id"],
                            building_id=i["building_id"],
                            uspd=i["uspd"]
                        )
                    )
            elif i['type'] == 'ZET_Thermometer':
                    self.devices.append(
                        Zet_Thermometer(
                            id=i["id"],
                            slave=i["slave"],
                            name=i["name"],
                            type=i["type"],
                            registers=i["registers"],
                            last_sensor = i["last_sensor"],
                            object_id=i["object_id"],
                            building_id=i["building_id"],
                            uspd=i["uspd"],
                            quantity=i["quantity"]
                        )
                    )
            elif i['type'] == 'ZET_Accelerometer':
                    self.devices.append(
                        Zet_Accelerometer(
                            id=i["id"],
                            slave=i["slave"],
                            name=i["name"],
                            type=i["type"],
                            registers=i["registers"],
                            object_id=i["object_id"],
                            building_id=i["building_id"],
                            uspd=i["uspd"]
                        )
                    )
            elif i['type'] == 'ZET_Hygrometer':
                    self.devices.append(
                        Zet_Hygrometer(
                            id=i["id"],
                            slave=i["slave"],
                            name=i["name"],
                            type=i["type"],
                            registers=i["registers"],
                            object_id=i["object_id"],
                            building_id=i["building_id"],
                            uspd=i["uspd"]
                        )
                    )

    def request_data(self):
        if not self.devices:
            print(f"\t{self.id} device list is empty!")
            return
        print(f"\t[*] Process converter: {self.name}")
        for i in self.devices:
            if i.type == "ZET_7054_Inclinometer":
                tk_raw_values = []
                print(f"\t\t[*] Process device: {i.name} slave: {i.slave_number}")
                client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number, timeout=30.0, debug=False, auto_open=True, auto_close=False) #Slave?
                x_high = client.read_holding_registers(i.x_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                x_low = client.read_holding_registers(i.x_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                y_high = client.read_holding_registers(i.y_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                y_low = client.read_holding_registers(i.y_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                if None in [x_high, x_low, y_high, y_low]:
                    print("\t\t\tNull received. Abort...")
                    continue
                # print(f"X_READED: \r\nhigh {x_high}\r\nlow {x_low}")
                # print(f"x_raw: high {x_high[0]} low {x_low[0]}")
                # print(f"y_raw: high {y_high[0]} low {y_low[0]}")
                x_decoded = i.decode(x_high[0], x_low[0])
                y_decoded = i.decode(y_high[0], y_low[0])
                print(f"\t\t\tx_decoded: {x_decoded}")
                print(f"\t\t\ty_decoded: {y_decoded}")
                tk_raw_values.append(x_decoded)
                tk_raw_values.append(y_decoded)
                measure_object = Collected_Measures(i, tk_raw_values)
                Measure_Storage.stored_measures.put(measure_object)
                client.close()
                time.sleep(0.5)
            elif i.type == "ZET_Thermometer":
                tk_raw_values = []
                # result_measures.append()
                print(f"\t\t[*] Process device: {i.name} slave: {i.slave_number}")
                client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number, timeout=30.0, debug=False, auto_open=True, auto_close=False) #Slave?
                for j in range(1, i.last_sensor + 1):
                    # print(f"Current reg is hex: {i.registers[j]} int: {int(i.registers[j],16)}")
                    tk_raw_measure = client.read_holding_registers(int(i.registers[j],16))
                    if tk_raw_measure == None:
                        print("\t\t\tNull received. Abort...")
                        continue
                    result_measure = i.decode(tk_raw_measure[0])
                    print(f"\t\t\t{j}: {result_measure}")
                    tk_raw_values.append(result_measure)
                if len(tk_raw_values) == i.quantity:
                    sensor_offset = len(tk_raw_values) - i.quantity
                    measure_object = Collected_Measures(i, tk_raw_values[sensor_offset:])
                    Measure_Storage.stored_measures.put(measure_object)
                client.close()
                time.sleep(0.5)
            elif i.type == "ZET_Accelerometer":
                acc_raw_values = []
                print(f"\t\t[*] Process device: {i.name} slave: {i.slave_number}")
                client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number, timeout=30.0, debug=False, auto_open=True, auto_close=False)
                counter = 0
                for j in i.registers:
                    acc_raw_value = client.read_holding_registers(j)
                    if acc_raw_value == None:
                        print("\t\t\tNull received.")
                        counter+=1
                        continue
                    acc_raw_values.append(acc_raw_value[0])
                    # print(f"\t\t\t{counter}: {acc_raw_value}")
                    counter+=1
                if len(acc_raw_values) == len(i.registers):
                    x_y_z = []
                    for j in range(len(acc_raw_values)):
                        if j not in [1, 7, 13]: # Индекс значения старшего байта замеров вибростойкости по x, y, z
                            continue
                        # print(f"high: {acc_raw_values[j]} low: {acc_raw_values[j-1]}")
                        decoded_value = i.decode(acc_raw_values[j], acc_raw_values[j-1])
                        x_y_z.append(
                            decoded_value
                        )
                    print(f"\t\t\tdecoded_x: {x_y_z[0]}", f"\t\t\tdecoded_y: {x_y_z[1]}", f"\t\t\tdecoded_z: {x_y_z[2]}", sep="\r\n")
                    measure_object = Collected_Measures(i, x_y_z)
                    Measure_Storage.stored_measures.put(measure_object)
                client.close()
                time.sleep(0.5)
            elif i.type == "ZET_Hygrometer":
                print(f"\t\t[*] Process device: {i.name} slave: {i.slave_number}")
                client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number, timeout=30.0, debug=False, auto_open=True, auto_close=False)
                counter = 0
                hg_result_measures = []
                hg_raw_values = []
                for j in i.registers:
                    hg_raw_value = client.read_holding_registers(j)
                    if hg_raw_value == None:
                        print("\t\t\tNull received. Abort...")
                        counter+=1                    
                        continue
                    hg_raw_values.append(hg_raw_value[0])
                    if len(hg_raw_values) == len(i.registers):
                        humidity = int(i.decode(hg_raw_values[1], hg_raw_values[0])) # относительная влажность.
                        temperature = round(i.decode(hg_raw_values[3], hg_raw_values[2]),2) # температура окружающей среды.
                        pressure = round(i.decode(hg_raw_values[5], hg_raw_values[4]),2) # атмосферное давление.
                        print(f"\t\t\tHumidity: {humidity}")
                        print(f"\t\t\tTemperature: {temperature}")
                        print(f"\t\t\tPressure: {pressure}")
                        hg_result_measures.append(humidity)
                        hg_result_measures.append(temperature)
                        hg_result_measures.append(pressure)
                        measure_object = Collected_Measures(i, hg_result_measures)
                        Measure_Storage.stored_measures.put(measure_object)
                    counter+=1
                ##
                client.close()
                time.sleep(0.5)
        return 0

class Zet_device(object):
    def __init__(self, id: str, slave: int, name: str, object_id: str, building_id: str, uspd: str) -> None:
        self.id = id
        self.slave_number = slave
        self.name = name
        self.object_id = object_id
        self.building_id = building_id
        self.uspd = uspd

class Zet_Inclinometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, x_low_high_regs, y_low_high_regs, object_id: str, building_id: str, uspd: str) -> None:
        super().__init__(id, slave, name, object_id, building_id, uspd)
        self.x_registers = x_low_high_regs # 20 - low | 21 - high
        self.y_registers = y_low_high_regs # 58 - low | 59 - high
        self.type = type

    def __str__(self):
        return f"Zet_Inclinomter: ID: {self.id}, Name: {self.name}, slave_number: {self.slave_number}"

    def decode(self, high_bytes, low_bytes):
        to_bytes = struct.pack('>HH', high_bytes, low_bytes)
        float_res = struct.unpack('>f', to_bytes)
        return float_res[0]
    
class Zet_Thermometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list, last_sensor:int, object_id:str, building_id:str, uspd: str, quantity: str) -> None:
        super().__init__(id, slave, name, object_id, building_id, uspd)
        self.registers = registers
        self.type = type
        self.last_sensor = last_sensor
        self.quantity = quantity
    
    def __str__(self):
        return f"Zet_Thermometer: ID: {self.id}, Name: {self.name}, slave_number: {self.slave_number}"

    def decode(self, raw_measure):
        to_bytes = struct.pack('>H', raw_measure)
        [decoded_measure] = struct.unpack('>h', to_bytes)
        return decoded_measure / 100
    
class Zet_Accelerometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list, object_id: str, building_id: str, uspd: str) -> None:
        super().__init__(id, slave, name, object_id, building_id, uspd)
        self.registers = registers
        self.type = type
        
    def __str__(self):
        return f"Zet_Accelerometer: ID: {self.id}, Name: {self.name}, slave_number: {self.slave_number}"

    def decode(self, high_bytes, low_bytes):
        b_meas = struct.pack('>HH', high_bytes, low_bytes)
        float_res = struct.unpack('>f', b_meas)
        return float_res[0]

class Zet_Hygrometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list, object_id: str, building_id: str, uspd: str) -> None:
        super().__init__(id, slave, name, object_id, building_id, uspd)
        self.registers = registers
        self.type = type
        
    def decode(self, high_bytes, low_bytes):
        to_bytes = struct.pack('>HH', high_bytes, low_bytes)
        float_res = struct.unpack('>f', to_bytes)
        return float_res[0]
        
    def __str__(self):
        return f"Zet_Hygrometer: ID: {self.id}, Name: {self.name}, slave_number: {self.slave_number}"
