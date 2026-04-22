
import serial

from time import sleep, time
import serial.tools.list_ports
import math
from pyfirmata import Arduino, util
import pyfirmata

def initialize():
    
    # automatic detection of comm port
    ports = serial.tools.list_ports.comports()

    commPort = 'None'
    for i in range(0, len(ports)):

        port = str(ports[i])
        if 'USB Serial Device' in port:
            commPort = port[3:5]
            

    if commPort != 'None':
        try:
            print(commPort)
            piqi = serial.Serial(
                port=f'COM{commPort}',
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
            )
        except Exception as e:
            raise e
    else:
        raise ValueError

    return piqi

def read_uart_data():

    piqi = initialize()

    byte_list = []
    # output_list = [0,0,0,0]

    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    # print(byte_list)

    if byte_list[0] == 5: # CHARGE STATUS
        CHS = byte_list[1] # convert decimal equivalent to power
        # print(f"CHS = {CHS:.2f} %")
        # output_list[0] = CHS
        output_list[0] = CHS
   
    if byte_list[0] == 3: # CONTROL ERROR
        CE = byte_list[1]
        # print(f"CE = {CE}")
        output_list[1] = CE

    if byte_list[0] == 109: # 0x6d trough
        trough = byte_list[1]
        # print(f"Accuracy (Trough) = {trough}")
        output_list[2] = trough
    
    if byte_list[0] == 127: # 0x7f peak
        peak = byte_list[1]
        # print(f"Accuracy (Peak) = {peak}")
        output_list[3] = peak

    # byte_list  = []
    return output_list


def read_uart(i):

    piqi = initialize()

    byte_list = []
    # output_list = [0,0,0,0]

    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    a = piqi.read(1)
    deci = int.from_bytes(a, "little")
    byte_list.append(deci)

    # print(byte_list)

    if byte_list[0] == 5: # CHARGE STATUS
        CHS = byte_list[1] # convert decimal equivalent to power
        # print(f"CHS = {CHS:.2f} %")
        # output_list[0] = CHS
        output_list[0] = CHS*100/256
   
    if byte_list[0] == 3: # CONTROL ERROR
        CE = byte_list[1]
        # print(f"CE = {CE}")
        output_list[1] = CE

    if byte_list[0] == 109: # 0x6d trough
        trough = byte_list[1]
        # print(f"Accuracy (Trough) = {trough}")
        output_list[2] = trough
    
    if byte_list[0] == 127: # 0x7f peak
        peak = byte_list[1]
        # print(f"Accuracy (Peak) = {peak}")
        output_list[3] = peak

    # byte_list  = []
    i+=1
    return output_list, i



def read_error(i):
    output_list, i = read_uart(i)
    # print(f"CHS = {output_list[0]}, CE = {output_list[1]}, 0x6D = {output_list[2]}, 0x7F = {output_list[3]}")
    print(f"CHS = {output_list[0]:.2f}%, CE = {output_list[1]}, 0x6D = {output_list[2]}, 0x7F = {output_list[3]}, i = {i}")



byte_list = []
output_list = [0,0,0,0]
i = 0
# while(1):
#     read_error(i)
    
   
    
     