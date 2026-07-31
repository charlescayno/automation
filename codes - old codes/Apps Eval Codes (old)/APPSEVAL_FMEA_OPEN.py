print("Charles Cayno | 08-Jul-2021")

import sys

if str(sys.argv[1]) == 'help':
    print("arguments:")
    print("LED, vin_list, test_list, pins")
    print()
    input()

# from powi.equipment import *

# board = pyfirmata.Arduino('COM8')
# iterator = util.Iterator(board)
# iterator.start()
# RELAY = board.get_pin('d:12:o')

# def short():
#     RELAY.write(1)
# def open():
#     RELAY.write(0)

"""COMMS ADDRESS"""
ac_source_address = 5
source_power_meter_address = 2 
load_power_meter_address = 1
eload_address = 8
scope_address = "10.125.10.170"

"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
from time import sleep, time
import os
waveform_counter = 0

"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
# pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

"""USER INPUT"""
LED = sys.argv[1] # 46, NL
vin = [90, 300]
vin = convert_argv_to_int_list(sys.argv[2])
test_list = convert_argv_to_int_list(sys.argv[3])
pins = str(sys.argv[4])
# 1 - Startup Short
# 2 - Running Short


print("CH1: IDS | CH2: VOUT | CH3: VR | CH4: IOUT")
ids_channel = 1
vout_channel = 2
vr_channel = 3
iout_channel = 4

test = pins
waveforms_folder = f'waveforms/{test}'

"""DEFAULT FUNCTIONS"""

def discharge_output():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    eload.channel[3].cc = 1
    eload.channel[3].turn_on()
    sleep(2)
    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()

"""CUSTOM FUNCTIONS FOR THIS TEST"""

def getPinMax(time_division=10):
    pin_list = []
    i = 0
    sleep(2)
    increment = 0.25
    while i != time_division*timeperdiv:
        # if test == 2: sleep(2)
        sleep(increment)
        i+=increment
        pin = f"{pms.power:.3f}"
        pin_list.append(pin)
    
    pin = f"{max(pin_list)}"
    print(f"Max Pin: {pin} W")

    return pin


def defaultScopeSettings():
    # default
    print("SCOPE SETTINGS:")
    scope.channel_scale(ids_channel, 2)
    scope.channel_scale(vout_channel, 10)
    scope.channel_scale(vr_channel, 10)
    scope.channel_scale(iout_channel, 0.25)

    scope.channel_position(vout_channel, -2)
    scope.channel_position(vr_channel, -2)
    scope.channel_position(ids_channel, -4)
    scope.channel_position(iout_channel, -4)

    scope.channel_BW(ids_channel, 500)
    scope.channel_BW(vout_channel, 20)
    scope.channel_BW(vr_channel, 500)
    scope.channel_BW(iout_channel, 20)
    
    scope.record_length(50E6)
    scope.time_position(10)
    scope.time_scale(2)
    print()

    scope.stop()
    
    



"""MAIN"""
print(f"{pins}")
print("1 - Startup Open")
print("2 - Running Open")


headers(test)

discharge_output()

test = 1
if test in test_list:

    condition = "Startup Open"

    defaultScopeSettings()

    scope.edge_trigger(ids_channel, .5, 'POS')

    input(f"Open {pins} pin. ")

    for voltage in vin:

        if voltage == 230: frequency = 50
        elif voltage == 265: frequency = 50
        else: frequency = 60
        timeperdiv = int(scope.get_horizontal()['scale'])



        scope.run_single()
        sleep(2*timeperdiv)

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        
        sleep(10*timeperdiv)

        discharge_output()





        ic_temp = input("Input IC temp: ")

        for i in range(5):


            if LED != 'NL': filename = f"{pins} pin - {condition}, {LED}V, {voltage}Vac {frequency}Hz, {ic_temp}degC, ({i}).png"
            else: filename = f"{pins} pin - {condition}, NL, {voltage}Vac {frequency}Hz, {ic_temp}degC, ({i}).png"


            y = input(">> Press ENTER to capture waveform. ")
            
            if y == '':
                scope.get_screenshot(filename, waveforms_folder)
                waveform_counter += 1
                print(filename)
                print()
            else:
                break

        print()
        input(">> Press to ENTER to continue testing... \n")


test = 2
if test in test_list:

    condition = "Running Open"

    defaultScopeSettings()

    scope.edge_trigger(iout_channel, 1.1, 'NEG')
    scope.time_position(20)

    for voltage in vin:

        if voltage == 230: frequency = 50
        elif voltage == 265: frequency = 50
        else: frequency = 60

        timeperdiv = int(scope.get_horizontal()['scale'])

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()

        sleep(2*timeperdiv)
        scope.run_single()
        sleep(2*timeperdiv)

        input(f"Open {pins} pin for {5*timeperdiv} seconds.")

        input(f"Short {pins} pin")

        discharge_output()

        ic_temp = input("Input IC temp: ")

        for i in range(5):


            if LED != 'NL': filename = f"{pins} pin - {condition}, {LED}V, {voltage}Vac {frequency}Hz, {ic_temp}degC, ({i}).png"
            else: filename = f"{pins} pin - {condition}, NL, {voltage}Vac {frequency}Hz, {ic_temp}degC, ({i}).png"


            y = input(">> Press ENTER to capture waveform. ")
            
            if y == '':
                scope.get_screenshot(filename, waveforms_folder)
                waveform_counter += 1
                print(filename)
                print()
            else:
                break

        print()
        input(">> Press to ENTER to continue testing... \n")


footers(waveform_counter)