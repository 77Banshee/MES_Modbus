import time
from serial import Serial
from modbus_tk.modbus_rtu import RtuMaster
import modbus_tk.defines as cst  # cst = constants
PORT = 'COM3'
serial_ = Serial(PORT)
modbus_master = RtuMaster(serial_)
modbus_master.set_timeout(5.0)
time.sleep(2.0)

response = modbus_master.execute(
    slave=3,
    function_code=cst.READ_HOLDING_REGISTERS,
    starting_address=1,
    quantity_of_x=10,
    output_value=[1]
)  # type: tuple

print(response)