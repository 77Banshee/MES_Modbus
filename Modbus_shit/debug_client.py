from pyModbusTCP.client import ModbusClient
import time


#ACC
#TG
#

def inclinometer_example():
    slaves = [19, 20, 21]

    for i in range(0, len(slaves)):
        print(f"Slave: {slaves[i]}")
        client = ModbusClient("192.168.9.13", 502, slaves[i], 30.0, True, True, False)

        x_high = client.read_holding_registers(21)
        print(f"x_high: {x_high}")
        x_low = client.read_holding_registers(20) 
        print(f"x_low: {x_low}") 
        y_high = client.read_holding_registers(59)
        print(f"y_high: {y_high}")
        y_low = client.read_holding_registers(58)
        print(f"y_low: {y_low}")
        print()
        client.close()
        time.sleep(2)
    
def thermometer_example():
    slaves = [26, 27, 28]
    
    regs = [0x1000,0x1010,0x1011,0x1012,0x1013,0x1014,0x1015,0x1016,0x1017,0x1018,0x1019,0x101a,0x101b,
            0x101c,0x101d,0x101e,0x101f,0x1020,0x1021,0x1022,0x1023,0x1100,0x1101,0x1102,0x1103,0x1104,
            0x1105,0x1106,0x1107,0x1108,0x1109,0x110a,0x110b,0x110c,0x110d,0x110e,0x110f,0x1110,0x1111,
            0x1112,0x1113,0x1200,0x1201,0x1202,0x1203,0x1204,0x1205,0x1206,0x1207,0x1208,0x1209,0x120a,
            0x120b,0x120c,0x120d,0x120e,0x120f,0x1210,0x1211,0x1212,0x1213,0x1214,0x1215,0x1216,0x1217,
            0x1218,0x1219,0x121a,0x121b,0x121c,0x121d,0x121e,0x121f,0x1220,0x1221,0x1222,0x1223,0x1224,
            0x1225,0x1226,0x1227,0x1228,0x1229,0x122a,0x122b,0x122c,0x122d,0x122e,0x122f,0x1230,0x1231,
            0x1232,0x1233,0x1234,0x1235,0x1236,0x1237,0x1238,0x1239,0x123a,0x123b,0x123c,0x123d,0x123e,
            0x123f,0x1240,0x1241,0x1242,0x1243,0x1244,0x1245,0x1246,0x1247,0x1248,0x1249,0x124a,0x124b,
            0x124c,0x124d,0x124e,0x124f,0x1250,0x1251,0x1252,0x1253,0x1254,0x1255,0x1256,0x1257,0x1258,
            0x1259,0x125a,0x125b,0x125c,0x125d,0x125e,0x125f,0x1260,0x1261,0x1262,0x1263]
    
    for j in slaves:
        print(f"Slave: {j}")
        client = ModbusClient("192.168.9.19", 502, j, 30.0, False, True, False)

        for i in regs:
            print(client.read_holding_registers(i))
        print()
        client.close()
        time.sleep(4)
        print()

def hygrometer_example():
    slave = 41
    regs = [20,21,58,59,96,97]
    client = ModbusClient("192.168.9.15", 502, slave, 30.0, False, True, False)
    for i in regs:
        print(client.read_holding_registers(i))
    print()
    client.close()
    time.sleep(2)
    print()
    
def accelerometer_example():
    regs = [20,21,44,45,46,47,58,59,82,83,84,85,96,97,120,121,122,123]

    slave = 4
    client = ModbusClient("192.168.9.16", 502, slave, 30.0, False, True, False)
    for i in regs:
        print(client.read_holding_registers(i))
    print()
    client.close()
    time.sleep(2)
    print()


if __name__ == "__main__":
    thermometer_example()