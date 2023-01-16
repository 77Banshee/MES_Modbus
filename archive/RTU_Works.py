import minimalmodbus
import serial
import time

instrument = minimalmodbus.Instrument('COM3', 1)  # port name, slave address (in decimal)
instrument.serial.port = 'COM3'                     # this is the serial port name
instrument.serial.baudrate = 19200         # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_ODD
instrument.serial.stopbits = 1
instrument.serial.timeout = 1        # seconds
instrument.address = 3                         # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU# rtu or ascii mode

while 1:
    result = instrument.read_float(21, 3, 4, byteorder=0)
    print(result)
    time.sleep(1)
