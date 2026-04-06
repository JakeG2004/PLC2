from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("127.0.0.1", port=5000)

if not client.connect():
    raise RuntimeError("Connection Faled")

DEVICE_ID = 1

# read coils
read_co = client.read_coils(0, count=8, device_id=DEVICE_ID)
print("Coils[0]-[7]: ", read_co.bits[:8])

# write coil
client.write_coil(0, value=False, device_id=DEVICE_ID);

# read coils
read_di = client.read_discrete_inputs(0, count=8, device_id=DEVICE_ID)
print("Coils[0]-[7]: ", read_di.bits[:8])

# Holding Registers
read_hr = client.read_holding_registers(0, count=5, device_id=DEVICE_ID);
print("Coils[0..4]", read_hr.registers)

# Write register
client.write_register(1, value=1234, device_id=DEVICE_ID)
read_hr = client.read_holding_registers(0, count=5, device_id=DEVICE_ID);
print("Coils[0..4]", read_hr.registers)

# Write multi registers
client.write_registers(2, [1, 2, 3], device_id=DEVICE_ID)
read_hr = client.read_holding_registers(0, count=5, device_id=DEVICE_ID);
print("Coils[0..4]", read_hr.registers)