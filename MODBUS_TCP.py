from pyModbusTCP.client import ModbusClient
import time
import struct

def convert(arg1, arg2):
    # b_res_little = struct.pack('<HH', arg1, arg2)
    b_res_big = struct.pack('>HH', arg1, arg2)

    # res_little = struct.unpack('<f', b_res_little)
    res_big = struct.unpack('>f', b_res_big)
    return res_big[0]


client = ModbusClient(
    host="192.168.9.11",
    port=502,
    unit_id=3,
    auto_open=True
)



# if __name__ == "__main__":
#     while 1:
#         y_values = client.read_holding_registers(58, 2)
#         print(y_values)
#         y_low = y_values[1]
#         y_high = y_values[0]
#         y_res = convert(y_low, y_high)
#         print(f"y: {y_res}")
#
#         x_values = client.read_holding_registers(20, 2)
#         x_low = x_values[1]
#         x_high = x_values[0]
#         x_res = convert(x_low, x_high)
#         print(f"x: {x_res}")
#         time.sleep(1)




client.write_multiple_registers(2, [1])
time.sleep(1)
client.write_multiple_registers(14, [10])
time.sleep(1)
client.write_multiple_registers(2, [3])
time.sleep(1)
res = client.read_holding_registers(14, 2)
print(res)