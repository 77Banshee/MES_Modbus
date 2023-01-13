from pyModbusTCP.client import ModbusClient
import struct
import json

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

class Converter_Repository():
    def __init__(self, path_to_cfg: str):
        self.converter_list = []
        with open(path_to_cfg, 'r') as f:
            self.json_config = json.load(f)
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
                            x_registers=i['registers']['x'], 
                            y_registers=i['registers']['y']
                        )
                    )
            elif i['type'] == 'Thermometer':
                    raise NotImplementedError('Zet_Converter.init_devices() THERMOMTER NOT IMPLEMENT')

    def receive_all(self):
        if not self.devices:
            print(f"{self.id} device list is empty!")
            return
        print(f"[*] Process converter: {self.name}")
        for i in self.devices:
            if i.type == "ZET_7054_Inclinometer":
                    print(f"[*] Process device: {i.name} slave: {i.slave_number}")
                    client = ModbusClient(host=self.ip_address, port=self.port, unit_id=i.slave_number) #Slave?
                    x_high = client.read_holding_registers(i.x_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    x_low = client.read_holding_registers(i.x_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    y_high = client.read_holding_registers(i.y_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
                    y_low = client.read_holding_registers(i.y_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.

                    if None in [x_high, x_low, y_high, y_low]:
                        print("Null received. Abort...")
                        continue
                    
                    x_decoded = i.decode(x_high[0], x_low[0])
                    y_decoded = i.decode(y_high[0], y_low[0])
                    print(f"x_raw: {x_decoded}")
                    print(f"y_raw: {y_decoded}")
                    
                    # print(f"{i.name} {i.type} | x: {i.decode(x_raw)} | y: {i.decode(y_raw)}")
            else:
                raise ValueError("[*] Wrong device type!")
# x_raw: [[16408], [43274]]
# y_raw: [[49431], [11310]]       

class Zet_Inclinometer(object):
    def __init__(self, id: str, slave: int, name, type, x_registers, y_registers):
        [self.id] = id,
        self.x_registers = x_registers
        self.y_registers = y_registers
        self.slave_number = slave
        self.name = name
        self.type = type

    def __str__(self):
        return f"Zet_Inclinomter: ID: {self.id}, x_registers: {self.x_registers}, y_registers: {self.y_registers}, slave_number: {self.slave_number}"

    def decode(self, high, low):
        to_bytes = struct.pack('>HH', high, low)
        float_res = struct.unpack('>f', to_bytes)
        return float_res[0]

    # Do i even need it?
    # def receive(self, ip, port, unit_id):
    #     client = ModbusClient(ip, port, unit_id)  # 0x03 register.
    #     x_raw_values = client.read_holding_registers(self.x_registers[0], 2)  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
    #     y_raw_values = client.read_holding_registers(self.y_registers[0], 2)
    #     return self.to_float(x_raw_values), self.to_float(y_raw_values) # X, Y


if __name__ == '__main__':
    print("__Modbus_client__")
    print("[* Init...]")
    cr = Converter_Repository("Config/converter.json")
    print("[* Config has loaded!]")
    for i in cr.converter_list:
        
        print(f"Converter: {i}")
        for j in i.devices:
            print(f"\tDevice: {j}")

    print("Start receive...")
    for i in cr.converter_list:
        i.receive_all()