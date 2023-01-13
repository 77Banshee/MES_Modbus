from pyModbusTCP.client import ModbusClient
import struct
import json

class Converter_Repository():
    def __init__(self, path_to_cfg: str):
        self.converter_list = []
        with open(path_to_cfg, 'r') as f:
            self.json_config = json.load(f)
        self.init_converter_list()

    def init_converter_list(self):
        converter_list_raw = self.json_config['converter']
        for i in converter_list_raw:
            self.converter_list.append(
                Zet_Converter(
                    i['ip_address'],
                    i['name'],
                    i['devices']
                )
            )

class Zet_Converter(object):
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
            match i['type']:
                case 'ZET_7054_Inclinometer':
                    self.devices.append(
                        Zet_Inclinometer(
                            i['id'], i['slave'], i['registers']['x'], i['registers']['y']
                        )
                    )
                case 'Thermometer':
                    raise NotImplementedError('Zet_Converter.init_devices() THERMOMTER NOT IMPLEMENT')

    def receive(self):
        if not self.devices:
            print(f"{self.id} device list is empty!")
            return
        client = ModbusClient(host=self.ip_address, port=self.port, unit_id=3)  # 0x03 register.
        x_high = client.read_holding_registers(self.y_registers[1])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
        x_low = client.read_holding_registers(self.y_registers[0])  # В struct pack/unpack передавать сначала 21 потом 20 регистр.


class Zet_Inclinometer(object):
    def __init__(self, id: str, slave: int, x_registers: [], y_registers: []):
        self.id = id,
        self.x_registers = x_registers
        self.y_registers = y_registers
        self.slave_number = slave

    def __str__(self):
        return f"Zet_Inclinomter: ID: {self.id}, x_registers: {self.x_registers}, y_registers: {self.y_registers}, slave_number: {self.slave_number}"

    def to_float(self, raw_values):
        to_bytes = struct.pack('>HH', raw_values[1], raw_values[0])
        float_res = struct.unpack('>f', to_bytes)
        return float_res[0]

    # def receive(self):
    #     client = ModbusClient(host="192.168.9.11", port=502, unit_id=3)  # 0x03 register.
    #     x_raw_values = client.read_holding_registers(self.x_registers[0], 2)  # В struct pack/unpack передавать сначала 21 потом 20 регистр.
    #     y_raw_values = client.read_holding_registers(self.y_registers[0], 2)
    #     return self.to_float(x_raw_values), self.to_float(y_raw_values) # X, Y

if __name__ == '__main__':
    print("__Modbus_client__")
    cr = Converter_Repository("Config/converter.json")
    for i in cr.converter_list:
        print(i)
        for j in i.devices:
            print(j)
