# Simple EEPROM reading.
import EasyMCP2221
from time import time, sleep
from misc_codes.equipment_settings import *
import struct

# Connect to MCP2221
mcp = EasyMCP2221.Device()

MEM_ADDR = 0x03


def read_eeprom_1_byte():
    data = mcp.I2C_read(
        addr = MEM_ADDR,
        size = 1)
    return data

def hex2dec(data):
    decimal = int.from_bytes(data, "little")
    return decimal

def get_hex(value):
    convert_string = int(value, base=16)
    convert_hex = hex(convert_string)
    return convert_hex, convert_string

def _sigfig(number, sigfig):
        try: a = float(f"{number:.{sigfig}f}")
        except: a = "NaN"
        return a

def combine_bytes(msb, lsb):
    combined = (msb<<8) | lsb
    return combined

def isense_adc_to_actual(isense):
    # iin = isense*6E-4
    iin = isense
    return _sigfig(iin, 4)

def vbus_adc_to_actual(vbus):
    vbulk = vbus
    return _sigfig(vbulk, 4)

def convert_from_byte(data):
    # print(data)
    return [struct.unpack('<f', bytes(data[i:i+4]))[0] for i in range(0, len(data), 4)]


def read_eeprom():
    
    byte_list = []
    eeprom_length = 10
    iin = 0
    vbulk = 0

    while(1):

        data = read_eeprom_1_byte()
        decimal = hex2dec(data)
        print(decimal)

        # if decimal == 1:
        #     byte_list.append(decimal)
            
        #     for i in range(eeprom_length-1):
        #         data = read_eeprom_1_byte()
        #         decimal = hex2dec(data)
        #         byte_list.append(decimal)
        #         print(len(byte_list))
            
        #     print(byte_list)
        #     ioutval = byte_list[3]
        #     voutval = byte_list[4]

        #     print(ioutval, voutval)
        #     # pin_adc = convert_from_byte([pin_byte_1, pin_byte_2, pin_byte_3, pin_byte_4])[0]
        #     # actual_pin = EQUIPMENT_FUNCTIONS().INPUT_POWER_POWER_METER()
        #     # # print(pin_adc, actual_pin, pin_adc/actual_pin)
        #     # print(f"Power Input (ADC) [assumed PF=0.434] = {pin_adc} W, Actual Power Input = {actual_pin} W, ADC/Actual Ratio = {pin_adc/actual_pin}")

        #     # print()
        #     # print()

        #     sleep(0.2)

        #     # break

        
        # byte_list=[]

    # return ioutval, voutval


EQUIPMENT_FUNCTIONS().AC_TURN_ON(120)
sleep(10)
read_eeprom()