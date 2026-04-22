print("CMC | 13-Aug-2021")

test = "First Power-up"
waveforms_folder = f'waveforms/{test}'

"""LIBRARIES"""
from time import time, sleep
import sys
import os
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
waveform_counter = 0

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2    
eload_address = 8
scope_address = "10.125.11.0"

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
led = LEDControl()


"""USER INPUT"""
led_list = [46,36,24]
vin_list = [90, 115, 230, 265, 277, 300]
test_list = [1] #Include test number for specific test: 1 - Startup, 2 - Normal
component = "LYT8368C"
"""DO NOT EDIT BELOW THIS LINE"""


"""GENERIC FUNCTIONS"""
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


def scope_settings_for_startup_operation():

    if component == "VOUT, VR":
        scope.position_scale(time_position = 10, time_scale = 0.1)
        scope.edge_trigger(3, 0.5, 'POS')
        scope.channel_settings(channel = 1, scale = 0.1, position = -4)
        scope.channel_settings(channel = 2, scale = 10, position = -4)
        scope.channel_settings(channel = 3, scale = 11, position = -4)
        scope.channel_settings(channel = 4, scale = 10, position = -4)
        scope.remove_zoom()

def scope_settings_for_normal_operation():
    pass

def startup_operation():

    global waveform_counter

    scope_settings_for_startup_operation()

    for LED in led_list:

        led.voltage(LED)

        for vin in vin_list:
            
            discharge_output()
            
            scope.run_single()
            
            sleep(2)
            
            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            sleep(2)

            filename = f'{LED}V, {vin}Vac, Startup.png'

            path = waveforms_folder + f'/{component}'
            if not os.path.exists(path): os.mkdir(path)
            path = waveforms_folder + f'/{component}/Startup'
            if not os.path.exists(path): os.mkdir(path)   

            scope.get_screenshot(filename, path)
            print(filename)
            waveform_counter += 1

            # input("Press ENTER to continue test.")

def normal_operation():

    global waveform_counter

    scope_settings_for_normal_operation()
    
    for LED in led_list:
        for vin in vin_list:
            
            discharge_output()
            sleep(2)
            
            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            sleep(3)
            
            scope.run_single()

            sleep(2)

            filename = f'{LED}V, {vin}Vac, Normal.png'

            path = waveforms_folder + f'/{component}'
            if not os.path.exists(path): os.mkdir(path)
            path = waveforms_folder + f'/{component}/Normal'
            if not os.path.exists(path): os.mkdir(path)

            scope.get_screenshot(filename, path)
            print(filename)
            waveform_counter += 1

def main():
    global waveform_counter

    test = 1 # startup
    if test in test_list: startup_operation()

    test = 2 # normal
    if test in test_list: print("Test Not Supported Yet.")
    # if test in test_list: normal_operation()
        

if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)