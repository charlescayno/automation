##################################################################################
"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.11.0"

"""USER INPUT"""
led_list = [46]
# led_list = [46]
vin_list = [100,120,230,265,277,300]
# vin_list = [230]
test_list = [1,2] # 1 - Startup, 2 - Normal
# test_list = [1]
# component = "VDS"
# component = "VCSN, VDSN"
# component = "PASSFET, SEC_DIODE"
component = "IBOOST, DRES, BOOSTFET, BOOST_DIODE"
condition = "- 200R, 100pF"

test = "Component Stress Analysis (Final)"
waveforms_folder = f'C:/Users/ccayno/Desktop/DER-945/waveforms/{test}'

"""DO NOT EDIT BELOW THIS LINE"""
##################################################################################

"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
import winsound as ws
from playsound import playsound
waveform_counter = 0

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
# control = MultiprotocolControl()

"""GENERIC FUNCTIONS"""
if not os.path.exists(waveforms_folder): os.mkdir(waveforms_folder)

def discharge_output():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    eload.channel[3].cc = 1
    eload.channel[3].turn_on()
    eload.channel[1].short_on()
    sleep(2)
    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()
    eload.channel[1].short_off()
    sleep(1)











def scope_settings_for_startup_operation():

    print("Startup Operation")

    scope.stop()
    scope.position_scale(time_position = 10, time_scale = 0.2)
    scope.edge_trigger(2, 50, 'POS')

    if component == "VDS":
        scope.edge_trigger(2, 300, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_settings(2, 100, -4, 'Vds')
        scope.channel_state(3, 'OFF')
        scope.channel_state(4, 'OFF')
        scope.add_zoom(rel_pos = 15.5, rel_scale = 15)
    
    if component == "VCSN, VDSN":
        scope.edge_trigger(3, 157, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_state(2, 'OFF')
        scope.channel_settings(3, 50, -1, 'Vcsn')
        scope.channel_settings(4, 100, -3, 'Vdsn')
        scope.add_zoom(rel_pos = 13.9, rel_scale = 10)
    
    if component == "PASSFET, SEC_DIODE":
        scope.edge_trigger(3, 50, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_settings(2, 20, -1, 'PassFET')
        scope.channel_settings(3, 100, -4, 'Sec Diode')
        scope.channel_state(4, 'OFF')
        scope.add_zoom(rel_pos = 20, rel_scale = 25) 
    
    if component == "IBOOST, DRES, BOOSTFET, BOOST_DIODE":
        scope.edge_trigger(2, 10, 'POS')
        scope.position_scale(time_position = 10, time_scale = 1)
        scope.channel_settings(1, 5, -3, 'Iboost')
        scope.channel_settings(2, 40, -4, 'Dres')
        scope.channel_settings(3, 20, -2, 'BoostFET')
        scope.channel_settings(4, 40, -1, 'Boost Diode')
        scope.add_zoom(rel_pos = 20, rel_scale = 25)
    
    sleep(2) 
    











def scope_settings_for_normal_operation():

    print("Normal Operation")

    scope.stop()
    scope.position_scale(time_position = 20, time_scale = 0.005)
    scope.edge_trigger(3, 3, 'POS')

    if component == "VDS":
        scope.edge_trigger(2, 300, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_settings(2, 100, -4, 'Vds')
        scope.channel_state(3, 'OFF')
        scope.channel_state(4, 'OFF')
        scope.add_zoom(rel_pos = 20, rel_scale = 0.1)

    if component == "VCSN, VDSN":
        scope.edge_trigger(3, 157, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_state(2, 'OFF')
        scope.channel_settings(3, 50, -1, 'Vcsn')
        scope.channel_settings(4, 100, -3, 'Vdsn')
        scope.add_zoom(rel_pos = 20, rel_scale = 0.1)

    if component == "PASSFET, SEC_DIODE":
        scope.edge_trigger(2, 15, 'POS')
        scope.channel_settings(1, 0.25, -4, 'Iout')
        scope.channel_settings(2, 20, -1, 'PassFET')
        scope.channel_settings(3, 100, -4, 'Sec Diode')
        scope.channel_state(4, 'OFF')
        scope.add_zoom(rel_pos = 20.12, rel_scale = 0.6)   
    
    if component == "IBOOST, DRES, BOOSTFET, BOOST_DIODE":
        scope.position_scale(time_position = 20, time_scale = 0.005)
        scope.edge_trigger(3, 70, 'POS')
        scope.channel_settings(1, 5, -2, 'Iboost')
        scope.channel_settings(2, 40, -4, 'Dres')
        scope.channel_settings(3, 20, -2, 'BoostFET')
        scope.channel_settings(4, 40, 2, 'Boost Diode')
        scope.add_zoom(rel_pos = 20, rel_scale = 0.3)

    sleep(2) 









def get_value(channel):
    labels, values = scope.get_measure(channel)
    max_value = float(values[0])
    max_value = float(f"{max_value:.2f}")
    return max_value


def export_scope_measurement(component, LED, vin, test_type):

    load = str(LED)
    input = str(vin)
    ch1_max = f"{get_value(1)}"
    ch2_max = f"{get_value(2)}"
    ch3_max = f"{get_value(3)}"
    ch4_max = f"{get_value(4)}"
    
    output_list = [load, input, ch1_max, ch2_max, ch3_max, ch4_max]
    # print(','.join(output_list))

    with open(f'{component} - {LED}V at {test_type}.txt', 'a+') as f:
        f.write(','.join(output_list))
        f.write('\n')






def startup_operation():

    global waveform_counter
    test_type = "Startup"

    scope_settings_for_startup_operation()
    
    for LED in led_list:
        if os.path.exists(f"{component} - {LED}V at {test_type}.txt"): os.remove(f"{component} - {LED}V at {test_type}.txt")
        prompt(f"Change LED load to {LED} Volts")

        for vin in vin_list:

            if vin == 300: count = 5
            else: count = 1

            for i in range(count):

                scope.run_single()
                sleep(2)
                ac.voltage = vin
                ac.frequency = ac.set_freq(vin)
                ac.turn_on()
                sleep(5)
                

                if component == "IBOOST, DRES, BOOSTFET, BOOST_DIODE": sleep(7)

                filename = f'{LED}V, {vin}Vac, {test_type}_{i}.png'

                path = waveforms_folder + f'/{component}'
                if not os.path.exists(path): os.mkdir(path)
                path = waveforms_folder + f'/{component}/{test_type}'
                if not os.path.exists(path): os.mkdir(path)
                path = waveforms_folder + f'/{component}/{test_type}/{LED}V {condition}'
                if not os.path.exists(path): os.mkdir(path)
                scope.get_screenshot(filename, path)
                print(filename)
                waveform_counter += 1

                export_scope_measurement(component, LED, vin, test_type)

                discharge_output()

    


def normal_operation():
    global waveform_counter
    test_type = "Normal"
    
    scope_settings_for_normal_operation()
    
    for LED in led_list:
        if os.path.exists(f"{component} - {LED}V at {test_type}.txt"): os.remove(f"{component} - {LED}V at {test_type}.txt")
        prompt(f"Change LED load to {LED} Volts")

        for vin in vin_list:

            if vin == 300: count = 5
            else: count = 1

            for i in range(count):
        
                discharge_output()

                sleep(2)
                ac.voltage = vin
                ac.frequency = ac.set_freq(vin)
                ac.turn_on()
                sleep(5)
                scope.run_single()
                sleep(5)

                filename = f'{LED}V, {vin}Vac, {test_type}_{i}.png'

                path = waveforms_folder + f'/{component}'
                if not os.path.exists(path): os.mkdir(path)
                path = waveforms_folder + f'/{component}/{test_type}'
                if not os.path.exists(path): os.mkdir(path)
                path = waveforms_folder + f'/{component}/{test_type}/{LED}V {condition}'
                if not os.path.exists(path): os.mkdir(path)
                scope.get_screenshot(filename, path)
                print(filename)
                waveform_counter += 1

                export_scope_measurement(component, LED, vin, test_type)
    
    discharge_output()


def main():
    global waveform_counter

    test = 1 # startup
    if test in test_list: startup_operation()

    test = 2 # normal
    if test in test_list: normal_operation()
        
if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)