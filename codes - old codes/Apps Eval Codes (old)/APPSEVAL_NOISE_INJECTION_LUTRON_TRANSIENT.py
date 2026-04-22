print("author: cmcayno | 23-Jul-2021")
print("\nSemi-automatic noise injector testing.")
print("You must load your own dfl file, and set trigger before hand before you run this program.")
print("Triggering level varies so it is more convenient to set it, \nthen run this script to collect your waveforms.\n\n")

# print("CH1 - NOISE")
# print("CH2 - IDS")
# print("CH3 - SCL/DIM")
# print("CH4 - VOUT")

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
scope_address_1 = "10.125.10.148"
scope_address_2 = "10.125.10.227"


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
scope1 = Oscilloscope(scope_address_1)
scope2 = Oscilloscope(scope_address_2)

# ac.voltage = 120
# ac.frequency = 60
# ac.turn_on()
# input()

### USER INPUT STARTS HERE ###
########################################################################
# SELECT LOAD CONFIGURATION
LED = "NL"
# LED = "46V"

# SELECT INPUT VOLTAGES
vin = [120, 230, 277]
# vin = [230, 277]
# vin = [120]
# vin = [230]
# vin = [277]

# SELECT PIN TO TEST
pin = "SCL(DIM)"

# SELECT NOISE LEVEL
noise = "+660" # mV

# SELECT RESISTOR LOAD
resistor_load = "3R9"

# SELECT LUTRON TRANSIENT CONDITION
# dim_level_1 = "10.6V(max)"
# dim_level_2 = "1.2V(min)"

# dim_level_1 = "1.2V(min)"
# dim_level_2 = "10.6V(max)"

# dim_level_1 = "10.6V(max)"
# dim_level_2 = "3V"

# dim_level_1 = "3V"
# dim_level_2 = "10.6V(max)"

dim_level_1 = "1.2V(min)"
dim_level_2 = "3V"

# manual = True
manual = False
test = f"Lutron Transient {dim_level_1}-{dim_level_2}, {LED}"
########################################################################
### USER INPUT ENDS HERE ###



"""DEFAULT FUNCTIONS"""
waveforms_folder = f'waveforms/{test}'

def discharge_output():
    ac.turn_off()
    
    eload.channel[1].cr = 100
    eload.channel[1].turn_on()
    eload.channel[2].cr = 100
    eload.channel[2].turn_on()
    eload.channel[3].cr = 100
    eload.channel[3].turn_on()
    
    sleep(1)
    
    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()

    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    eload.channel[3].cc = 1
    eload.channel[3].turn_on()
    
    sleep(1)

    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()


def scope_config():
    scope1.stop()
    scope2.stop()
    scope1.time_scale(2)
    scope2.time_scale(2)
    
    # scope1.channel_settings(channel=1, scale=1, position=0)
    # scope1.channel_settings(1, 1, 0)

"""MAIN"""

scope_config()
discharge_output()

headers(test)

for voltage in vin:

    if voltage == 230: frequency = 50
    elif voltage == 265: frequency = 50
    else: frequency = 60

    input(f"\n>> Change lutron dim level to {dim_level_1}.\n")

    ac.voltage = voltage
    ac.frequency = frequency
    ac.turn_on()

    scope1.run_single()
    scope2.run_single()



    if manual:
        input(f"\n>> Change lutron dim level to {dim_level_2}.\n")
        input("Start capturing waveforms? \n")
        discharge_output()

        print("Collect waveforms in SCOPE1.")
        i = 0
        while '' == input():
            filename = f"Lutron Transient {dim_level_1}-{dim_level_2}, {LED}, {noise}mV (at {resistor_load}), {voltage}Vac, scope1 ({i}).png"
            scope1.get_screenshot(filename, waveforms_folder)
            waveform_counter += 1
            i += 1
            print(filename)

        print("Collect waveforms in SCOPE2.")
        i = 0
        while '' == input():
            filename = f"Lutron Transient {dim_level_1}-{dim_level_2}, {LED}, {noise}mV (at {resistor_load}), {voltage}Vac, scope2 ({i}).png"
            scope2.get_screenshot(filename, waveforms_folder)
            waveform_counter += 1
            i += 1
            print(filename)
    



    if not manual:
        input(f"\n>> Change lutron dim level to {dim_level_2}.\n")
        input("Start capturing waveforms? \n")
        filename = f"Lutron Transient {dim_level_1}-{dim_level_2}, {LED}, {noise}mV (at {resistor_load}), {voltage}Vac, scope1.png"
        scope1.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)

        filename = f"Lutron Transient {dim_level_1}-{dim_level_2}, {LED}, {noise}mV (at {resistor_load}), {voltage}Vac, scope2.png"
        scope2.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)


    discharge_output()
footers(waveform_counter)