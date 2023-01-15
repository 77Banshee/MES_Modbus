from pyModbusTCP.client import ModbusClient
import struct
import json
import time
import queue

class Measure_Storage(object):
    stored_measures = queue.Queue()

class Collected_Measures(object):
    """Clase for store collected measures from devices.

    Args:
        device_instance: instace of measured device.
        measures: list of measures. 
        Order:
            Inclinomter: [x, y]
            Thermomter: [first-last sensor]
            Accelerometer: ?
            Hygrometer: ?
    """
    def __init__(self, device_instance, measures) -> None:
        measures = []
        dev_type = device_instance.type
        dev_name = device_instance.name
    def get_formatted_measures(self):
        print("get_formatted_measures Not implemented!")

class Converter_Repository(object):
    def __init__(self, json_config: str):
        self.converter_list = []
        self.json_config = json_config
        self.init_converter_list()

    def init_converter_list(self):
        converter_list_raw = self.json_config["converters"]
        for i in range(0, len(converter_list_raw)):
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

    def __str__(self):
        return f"Zet_Converter: Name: {self.name}, ip_address: {self.ip_address}"

    def init_devices(self, sensor_list_raw):
        for i in sensor_list_raw:
            if i['type'] == 'ZET_7054_Inclinometer':
                    self.devices.append(
                        Zet_Inclinometer(
                            id=i["id"],
                            type=i["type"],
                            name=i["name"],
                            slave=i['slave'],
                            x_low_high_regs=i['registers']['x'], 
                            y_low_high_regs=i['registers']['y']
                        )
                    )
            elif i['type'] == 'ZET_thermometer':
                    raise NotImplementedError('Zet_Converter.init_devices() THERMOMTER NOT IMPLEMENT')

    def request_data(self):
        if not self.devices:
            print(f"\t{self.id} device list is empty!")
            return
        print(f"\t[*] Process converter: {self.name}")
        for i in self.devices:
            if i.type == "ZET_7054_Inclinometer":
                    print(f"\t\t[*] Process device: {i.name} slave: {i.slave_number}")
                    client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number, timeout=30.0, debug=False, auto_open=True, auto_close=False) #Slave?
                    x_high = client.read_holding_registers(i.x_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    x_low = client.read_holding_registers(i.x_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    y_high = client.read_holding_registers(i.y_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    y_low = client.read_holding_registers(i.y_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.

                    if None in [x_high, x_low, y_high, y_low]:
                        print("\t\t\tNull received. Abort...")
                        continue
                    
                    x_decoded = i.decode(x_high[0], x_low[0])
                    y_decoded = i.decode(y_high[0], y_low[0])
                    print(f"\t\t\tx_decoded: {x_decoded}")
                    print(f"\t\t\ty_decoded: {y_decoded}")
                    measure_object = Collected_Measures(i, [x_decoded, y_decoded])
                    Measure_Storage.stored_measures.put(measure_object)
                    client.close()
                    time.sleep(2)
                    
                    # print(f"{i.name} {i.type} | x: {i.decode(x_raw)} | y: {i.decode(y_raw)}")
            else:
                raise ValueError("[*] Wrong device type!")

class Zet_device(object):
    def __init__(self, id: str, slave: int, name) -> None:
        self.id = id
        self.slave_number = slave
        self.name = name

class Zet_Inclinometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, x_low_high_regs, y_low_high_regs) -> None:
        super().__init__(id, slave, name)
        self.x_registers = x_low_high_regs # 20 - low | 21 - high
        self.y_registers = x_low_high_regs # 58 - low | 59 - high
        self.type = type

    def __str__(self):
        return f"Zet_Inclinomter: ID: {self.id}, x_registers: {self.x_registers}, y_registers: {self.y_registers}, slave_number: {self.slave_number}"

    def decode(self, high_bytes, low_bytes):
        to_bytes = struct.pack('>HH', high_bytes, low_bytes)
        float_res = struct.unpack('>f', to_bytes)
        return float_res[0]
    
class Zet_Thermometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list) -> None:
        super().__init__(id, slave, name)
        self.registers = registers
        self.type = type

    def decode(self):
        print(f"{self.type} {self.name} not implemented! Skip...")
    
class Zet_Accelerometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list) -> None:
        super().__init__(id, slave, name)
        self.registers = registers
        self.type = type

    def decode(self):
        print(f"{self.type} {self.name} not implemented! Skip...")

class Zet_Hygrometer(Zet_device):
    def __init__(self, id: str, slave: int, name:str, type:str, registers:list) -> None:
        super().__init__(id, slave, name)
        self.registers = registers
        self.type = type

    def decode(self):
        print(f"{self.type} {self.name} not implemented! Skip...")
