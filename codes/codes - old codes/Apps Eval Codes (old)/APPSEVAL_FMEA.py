print("Charles Cayno | 08-Jul-2021")

import sys

if str(sys.argv[1]) == 'help':
    print("arguments:")
    print("LED, vin_list, test_list, pins")
    print()
    input()

from powi.equipment import *

board = pyfirmata.Arduino('COM8')
iterator = util.Iterator(board)
iterator.start()
RELAY = board.get_pin('d:12:o')

def short():
    RELAY.write(1)
def open():
    RELAY.write(0)

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
pml = PowerMeter(load_power_meter_address)
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


print("CH1: VDS | CH2: VOUT | CH3: VR | CH4: IOUT")
vds_channel = 1
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
    scope.channel_scale(vout_channel, 10)
    scope.channel_scale(vr_channel, 10)
    scope.channel_position(vout_channel, -2)
    scope.channel_position(vr_channel, -2)
    scope.channel_position(vds_channel, -3)
    scope.channel_position(iout_channel, -4)
    scope.stop()
    
    



"""MAIN"""
print(f"{pins}")
print("1 - Startup Short")
print("2 - Running Short")


headers(test)

discharge_output()

test = 1
if test in test_list:

    condition = "Startup Short"

    defaultScopeSettings()

    scope.time_position(10)
    scope.time_scale(2)

    scope.edge_trigger(vds_channel, 50, 'POS')
    scope.channel_scale(iout_channel, 0.25)

    # special case: FW-DNC (NL)
    if pins == 'FW-DNC':
        scope.time_scale(4)
        scope.channel_position(vout_channel, -3)
        scope.channel_position(vr_channel, -3)

    if pins == 'HSG-VR':
        scope.channel_position(vout_channel, 0)
        scope.channel_position(vr_channel, 0)
        scope.channel_scale(vout_channel, 5)
        scope.channel_scale(vr_channel, 5)

    for voltage in vin:

        if voltage == 230: frequency = 50
        elif voltage == 265: frequency = 50
        else: frequency = 60
        timeperdiv = int(scope.get_horizontal()['scale'])

        short()
        
        scope.run_single()

        sleep(5)

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()

        # soak(10*timeperdiv)
        pin = getPinMax(time_division=10)
        # sleep(9*timeperdiv)
        # pin = f"{pms.power:.3f}"
        # sleep(1*timeperdiv)

        
        sleep(2)

        

        discharge_output()

        for i in range(5):

            if LED != 'NL': filename = f"{voltage}Vac {frequency}Hz, {LED}V, {pins} {condition}, Pinmax={pin}W ({i}).png"
            else: filename = f"{voltage}Vac {frequency}Hz, NL, {pins} {condition}, Pinmax={pin}W ({i}).png"

            y = input(">> Press ENTER to capture waveform. ")
            
            if y == '':
                scope.get_screenshot(filename, waveforms_folder)
                waveform_counter += 1
                print(filename)
                print()
            else:
                break


        print()


test = 2
if test in test_list:

    condition = "Running Short"

    defaultScopeSettings()
    
    scope.time_position(20)
    scope.time_scale(2)

    # if LED == 'NL': scope.time_scale(4)

    trigger_channel = str(input("Trigger Channel: ")).lower()
    if trigger_channel == 'vds': trigger_channel = 1
    if trigger_channel == 'vout': trigger_channel = 2
    if trigger_channel == 'vr': trigger_channel = 3
    if trigger_channel == 'iout': trigger_channel = 4
    trigger_level = float(input("Trigger Level: "))
    trigger_edge = str(input("Trigger Edge: ")).upper()

    scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)
    scope.channel_scale(iout_channel, 0.5)

    for voltage in vin:
        if voltage == 230: frequency = 50
        elif voltage == 265: frequency = 50
        else: frequency = 60
        timeperdiv = int(scope.get_horizontal()['scale'])
        
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()

        sleep(5)
        if LED == 'NL': sleep(3)


        scope.run_single()
        sleep(5)

        short()
        
        pin = getPinMax(time_division=4)

        open()

        sleep(10)
        if LED == 'NL': sleep(10)

        discharge_output()

        for i in range(5):

            if LED != 'NL': filename = f"{voltage}Vac {frequency}Hz, {LED}V, {pins} {condition}, Pinmax={pin}W ({i}).png"
            else: filename = f"{voltage}Vac {frequency}Hz, NL, {pins} {condition}, Pinmax={pin}W ({i}).png"

            y = input(">> Press ENTER to capture waveform. ")
            
            if y == '':
                scope.get_screenshot(filename, waveforms_folder)
                waveform_counter += 1
                print(filename)
                print()
            else:
                break
            
        print()


footers(waveform_counter)