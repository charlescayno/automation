print("author: cmcayno | 17-Jul-2021")
print("\nSemi-automatic noise injector testing.")
print("You must load your own dfl file, and set trigger before hand before you run this program.")
print("Triggering level varies so it is more convenient to set it, \nthen run this script to collect your waveforms.\n\n")

print("CH1 - NOISE")
print("CH2 - IDS")
print("CH3 - SCL/DIM")
print("CH4 - VOUT")

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.148"


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
# vin = [277]

# SELECT PIN TO TEST
pin = "SCL(DIM)"

# SELECT NOISE LEVEL
noise = "+660" # mV

# SELECT TEST TYPE
test_type = "Normal"
# test_type = "Startup"

# SELECT RESISTOR LOAD
resistor_load = "2R"

# SELECT LUTRON VOLTAGE
# dim_level = "10.6V"
dim_level = "5V"
# dim_level = "3V"
# dim_level = "1.2V"

scope.edge_trigger(1, 0.7, 'POS')
# scope.edge_trigger(1, -0.4, 'NEG')

# manual = True
manual = False
test = f"{pin} {test_type} {LED} - LUTRON (STEADY-STATE)"
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

def noload_scope_config():

    if dim_level == "10.6V":
        scope.channel_settings(channel = 1, scale = 1, position = 0)
        scope.channel_settings(channel = 2, scale = 2, position = -4)
        scope.channel_settings(channel = 3, scale = 2, position = -2)
        scope.channel_settings(channel = 4, scale = 10, position = -4)


    if dim_level == "5V":
        scope.channel_settings(channel = 1, scale = 1, position = 0)
        scope.channel_settings(channel = 2, scale = 2, position = -4)
        scope.channel_settings(channel = 3, scale = 2, position = 1)
        scope.channel_settings(channel = 4, scale = 10, position = -4)

    if dim_level == "3V":
        scope.channel_settings(channel = 1, scale = 1, position = 0)
        scope.channel_settings(channel = 2, scale = 2, position = -4)
        scope.channel_settings(channel = 3, scale = 2, position = 1)
        scope.channel_settings(channel = 4, scale = 10, position = -4)

    if dim_level == "1.2V":
        scope.channel_settings(channel = 1, scale = 1, position = 0)
        scope.channel_settings(channel = 2, scale = 2, position = -4)
        scope.channel_settings(channel = 3, scale = 2, position = 1)
        scope.channel_settings(channel = 4, scale = 10, position = -4)


def configure_scope():
    if test_type == "Startup":
        scope.time_scale(2)
        scope.edge_trigger(trigger_source = 2, trigger_level = 0.5, trigger_slope = 'POS')
        scope.write("LAYout:ZOOM:REM 'Diagram1', 'MyZoom1'")


        if LED == "NL":
            noload_scope_config()
            if dim_level == "5V": scope.channel_settings(channel = 3, scale = 2, position = -1)
            

        else:

            if dim_level == "10.6V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = 1)
                scope.channel_settings(channel = 4, scale = 0.3, position = -3)


            if dim_level == "5V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = -1)
                scope.channel_settings(channel = 4, scale = 0.1, position = -4)

            if dim_level == "3V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = 1)
                scope.channel_settings(channel = 4, scale = 0.05, position = -4)

            if dim_level == "1.2V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = 1)
                scope.channel_settings(channel = 4, scale = 0.01, position = -4)


    if test_type == "Normal":
        scope.time_scale(1E-3)

        scope.write("LAYout:ZOOM:ADD 'Diagram1', VERT, OFF, -100e-6, 100e-6, -0.1, 0.05, 'MyZoom1'")
        scope.write("LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'MyZoom1', 2")
        scope.write("LAYout:ZOOM:VERT:REL:SPAN 'Diagram1', 'MyZoom1', 100")
        scope.write("LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'MyZoom1', 20")

        if LED == "NL":
            noload_scope_config()

            if dim_level == "10.6V": scope.channel_settings(channel = 3, scale = 2, position = -2)
            if dim_level == "5V": scope.channel_settings(channel = 3, scale = 2, position = 1)
            if dim_level == "3V": scope.channel_settings(channel = 3, scale = 2, position = 2)
            if dim_level == "1.2V": scope.channel_settings(channel = 3, scale = 2, position = 3)

            
        else:

            if dim_level == "10.6V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = -4)
                scope.channel_settings(channel = 4, scale = 0.3, position = -3)


            if dim_level == "5V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = -1)
                scope.channel_settings(channel = 4, scale = 0.1, position = -4)

            if dim_level == "3V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 2, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = 2)
                scope.channel_settings(channel = 4, scale = 0.05, position = -4)

            if dim_level == "1.2V":
                scope.channel_settings(channel = 1, scale = 1, position = 0)
                scope.channel_settings(channel = 2, scale = 0.5, position = -4)
                scope.channel_settings(channel = 3, scale = 2, position = 2)
                scope.channel_settings(channel = 4, scale = 0.02, position = -4)


"""MAIN"""

headers(test)
discharge_output()
scope.stop()

configure_scope()

for voltage in vin:

    if voltage == 230: frequency = 50
    elif voltage == 265: frequency = 50
    else: frequency = 60

    if test_type == "Normal":
        
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        sleep(5)
        scope.run_single()
        sleep(3)
        if manual: input("Press ENTER to continue...")
        # if LED == "NL": pass
        # else: input(">> Kuntento ka na ba sa nakuha mo? Press ENTER kung oo!")
        # input(">> Kuntento ka na ba sa nakuha mo? Press ENTER kung oo!")
    
    if test_type == "Startup":
        
        discharge_output()
        discharge_output()
        scope.run_single()
        sleep(5)
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        sleep(20)
        if manual: input("Press ENTER to continue...")
        # input()
    
    filename = f"{pin} {test_type}, {noise}mV noise, {LED}, {voltage}Vac {frequency}Hz, {resistor_load} resistor, Lutron Dim Level = {dim_level}.png"
    scope.get_screenshot(filename, waveforms_folder)
    waveform_counter += 1
    print(filename)

    sleep(2)
    discharge_output()
    sleep(2)


footers(waveform_counter)