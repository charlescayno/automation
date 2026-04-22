
import serial

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()
# for i in range(0, len(ports)):
#     port = str(ports[i])
#     print(port)


port=input(">> Enter COM PORT number: ")


piqi = serial.Serial(
    port=f'COM{port}',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)

byte_list = []

while(1):
    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    if byte_list[0] == 4:
        power = byte_list[1]*5/128 # convert decimal equivalent to power
        print(f"RP8 = {power} W")
   
    if byte_list[0] == 127: # x7F == 127
        accuaracy = byte_list[1]
        if byte_list[1] == 10 or byte_list[1] == 11:
            accuaracy = 10
        print(f"Accuracy = {accuaracy*100/10} %")

    byte_list  = []