print("author: cmcayno | 23-Jul-2021")

print("Semi-automatic noise injector testing.")
print("You must load your own dfl file, and set trigger before hand before you run this program.")
print("Triggering level varies so it is more convenient to set it, then run this script to collect your waveforms.\n")

print("SCOPE1")
print("CH1 = VOUT")
print("CH2 = IDS")
print("CH3 = SDA/SET")
print("CH4 = IOUT")
print("\nSCOPE2")
print("CH3 = VR")


# COMMS
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.148"
scope2_address = "10.125.10.227"

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
scope2 = Oscilloscope(scope2_address)

### USER INPUT STARTS HERE ###
########################################################################

# SELECT LOAD CONFIGURATION
# LED = "NL"
LED = "24V"
# LED = "46V"

# SELECT INPUT VOLTAGES
vin = [90, 115, 230, 265, 277, 300]
# vin = [120, 230, 277]
# vin = [230, 265, 277]
# vin = [120, 277]
# vin = [230]
# SELECT PIN TO TEST
# pin = "SCL(DIM)"
# pin = "SDA(SET)"
pin = "BPS"

# SELECT NOISE LEVEL
# noise = "-660mV"
# noise = "+660mV"  
# noise = "+330mV"
noise = "-330mV"      



# SELECT TEST TYPE
# test_type = "Normal"
test_type = "Startup"

# SELECT RESISTOR LOAD
# resistor_load = "3R9"
resistor_load = "4R7"



noise_injector = True
# noise_injector = False

if noise_injector:
    test = f"{pin} {test_type} {LED} w probe (dc source)"

    # auto-adjust triggering
    noise_value = int(noise.strip("mV"))/1000 #V
    if noise_value > 0: noise_slope = 'POS'
    if noise_value < 0: noise_slope = 'NEG'
    scope.edge_trigger(3, noise_value, noise_slope)

if not noise_injector:
    scope.edge_trigger(2, 0.5, 'POS')
    test = f"{pin} {test_type} {LED} wo probes, wo noise injector"
waveforms_folder = f'waveforms/{test}'
########################################################################
### USER INPUT ENDS HERE ###


"""DEFAULT FUNCTIONS"""

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
    
    sleep(3)

    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()

"""CUSTOM FUNCTIONS FOR THIS TEST"""   
    
def remove_zoom():
    scope.write("LAYout:ZOOM:REM 'Diagram1', 'MyZoom1'")

def add_zoom():
    scope.write("LAYout:ZOOM:ADD 'Diagram1', VERT, OFF, -100e-6, 100e-6, -0.1, 0.05, 'MyZoom1'")
    scope.write("LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'MyZoom1', 2")
    scope.write("LAYout:ZOOM:VERT:REL:SPAN 'Diagram1', 'MyZoom1', 100")
    scope.write("LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'MyZoom1', 20")


def noload_scope_config():
    # channel, scale, position
    scope.channel_settings(1, 10, -3)
    scope.channel_settings(2, 2, -4)
    scope.channel_settings(3, 1, 3) # noise
    scope.channel_settings(4, 0.4, -3)
    scope2.channel_settings(3, 10, -4) # vr

    if noise_value < 0: scope.channel_settings(3, 1, 4) # noise
    if noise_value > 0: scope.channel_settings(3, 1, 3) # noise

def led46V_scope_config():
    scope.channel_settings(1, 10, -4) # vout
    scope.channel_settings(2, 2, -4) # ids
    scope.channel_settings(3, 1, 3) # noise
    scope.channel_settings(4, 0.3, -4) # iout
    scope2.channel_settings(3, 10, -4) # vr

def led24V_scope_config():
    scope.channel_settings(1, 10, 1) # vout
    scope.channel_settings(2, 2, -4) # ids
    scope.channel_settings(3, 1, -2) # bps
    scope.channel_settings(4, 0.25, -4) # iout
    scope2.channel_settings(3, 10, -4) # vr
    


def configure_scope():
    scope.stop()
    scope2.stop()

    if test_type == "Startup":
        scope.time_scale(2)
        scope2.time_scale(2)
        scope.edge_trigger(2, 0.5, 'POS')
        remove_zoom()
        if LED == "NL": noload_scope_config()          
        elif LED == '46V':
            led46V_scope_config()
            scope.channel_settings(1, 10, -1) # vout
        else: # 24V
            led24V_scope_config()
            # scope.channel_settings(1, 10, -3) # vout

    if test_type == "Normal":
        scope.time_scale(1E-3)
        scope2.time_scale(1E-3)
        add_zoom()
        if LED == "NL": noload_scope_config()
        elif LED == '46V': led46V_scope_config()
        else: led24V_scope_config()


"""MAIN"""

headers(test)
discharge_output()
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
        scope2.run_single()
        scope.run_single()
        sleep(3)
    
    if test_type == "Startup":
        discharge_output()
        discharge_output()
        scope2.run_single()
        scope.run_single()
        sleep(5)
        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        sleep(20)

    
    vout = f"{pml.voltage:.3f}"
    iout = f"{pml.current*1000:.2f}"

    if noise_injector:

        filename = f"{LED}, {voltage}VAC, {noise}, {resistor_load}, scope1, {vout}V, {iout}mA.png"
        scope.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)

        filename = f"{LED}, {voltage}VAC, {noise}, {resistor_load}, scope2, {vout}V, {iout}mA.png"
        scope2.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)

    if not noise_injector:

        filename = f"{LED}, {voltage}VAC, scope1, {vout}V, {iout}mA.png"
        scope.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)

        filename = f"{LED}, {voltage}VAC, scope2, {vout}V, {iout}mA.png"
        scope2.get_screenshot(filename, waveforms_folder)
        waveform_counter += 1
        print(filename)
    
    discharge_output()
    sleep(2)

footers(waveform_counter)