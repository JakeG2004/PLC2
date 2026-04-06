from pymodbus.server import StartTcpServer
from pymodbus import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext

def run_server():
    # number of registers to populate
    num_reg = 200

    # initialize the data
    device = ModbusDeviceContext (
        di = ModbusSequentialDataBlock(0, [0, 1] * (num_reg // 2)),
        co = ModbusSequentialDataBlock(0, [1] * num_reg),
        hr = ModbusSequentialDataBlock(0, [17] * num_reg),
        ir = ModbusSequentialDataBlock(0, [18] * num_reg)
    )

    context = ModbusServerContext(devices=device, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = "Not Allen Bradley"
    identity.ProductCode = "ABS" # A boring  simulator
    identity.ProductName = "PymodbusSim"
    identity.ModelName = "Model_1"

    StartTcpServer(context=context, identity=identity, address=("127.0.0.1", 5000))

    return True

def main():
    print("PyModbus TCP server started")
    run_server()

if __name__ == "__main__":
    main()