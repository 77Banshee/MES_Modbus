import serial
import time

with serial.Serial(
     port='COM3',
     baudrate=19200,
     parity=serial.PARITY_ODD,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=1
     ) as ser:
    print(f"{ser.name}: isOpen {ser.is_open}")
    while 1:
        buffer = ser.read(10)
        print(buffer)
