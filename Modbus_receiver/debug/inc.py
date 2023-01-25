import struct
from pyModbusTCP import client
import time

if __name__ == '__main__':
    ip = "192.168.9.13"
    port = 502
    slave = 19
    c = client.ModbusClient(ip, port, slave, 30, auto_close=True, auto_open=True)
    reg_1 = c.read_holding_registers(20)
    print(reg_1)
    time.sleep(0.5)
    reg_2 = c.read_holding_registers(21)
    print(reg_2)
    time.sleep(0.5)
    reg_3 = c.read_holding_registers(58)
    print(reg_3)
    time.sleep(0.5)
    reg_4 = c.read_holding_registers(59)
    print(reg_4)
    c.close()
    
    b_arr_x = bytearray()
    b_arr_y = bytearray()
    
    b_reg_1 = struct.pack('H', reg_1[0])
    b_reg_2 = struct.pack('H', reg_2[0])
    b_reg_3 = struct.pack('H', reg_3[0])
    b_reg_4 = struct.pack('H', reg_4[0])

    b_arr_x.append(b_reg_1[0])
    b_arr_x.append(b_reg_2[0])
    
    b_arr_y.append(b_reg_3[0])
    b_arr_y.append(b_reg_4[0])
    
    print(b_arr_x)
    
    # unp1 = int.from_bytes(b_arr_x, 'little')
    # unp2 = int.from_bytes(b_arr_x, 'big')
    x_fl_res_l = struct.unpack('f', b_arr_x)
    x_fl_res_b = struct.unpack('>f', b_arr_x)
    print(f"x_l: {x_fl_res_l}")
    print(f"x_b: {x_fl_res_b}")
    y_fl_res_l = struct.unpack('f', b_arr_y)
    y_fl_res_b = struct.unpack('>f', b_arr_y)
    print(f"y_l: {y_fl_res_l}")
    print(f"y_b: {y_fl_res_b}")
    