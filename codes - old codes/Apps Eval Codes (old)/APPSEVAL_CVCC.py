"""OCTOBER 3, 2021"""
### USER INPUT #######################################
led_list = [46]
vin_list = [90,115,230,277,300]
cp_list = [0,1,2,3] # 0 - 100%, 1 - 85%, 2 - 75%, 3 - 60%
test_list = [1,2] # 1 - min to max, 2 - max to min
test = f"CVCC"
waveforms_folder = f'waveforms/{test}'

"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
import os
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, footers, waveform_counter, soak, convert_argv_to_int_list
waveform_counter = 0

"""INITIALIZE EQUIPMENT"""
ac = ACSource(5)
# pms = PowerMeter(1)
# pml = PowerMeter(2)
eload = ElectronicLoad(8)
# scope = Oscilloscope('10.125.10.148')
# led = LEDControl()

def discharge_output():
    ac.turn_off()
    
    for i in range(1,6):
        eload.channel[i].cr = 100
        eload.channel[i].turn_on()
    
    sleep(1)

    for i in range(1,6):
        eload.channel[i].turn_off()
    
    sleep(1)

    for i in range(1,6):
        eload.channel[i].cc = 1
        eload.channel[i].turn_on()
    
    sleep(1)

    for i in range(1,6):
        eload.channel[i].turn_off()

    sleep(1)

from AUTOGUI_CONFIG import *
from time import sleep, time
import os.path
from os import path
import math

ate_gui = AutoguiCalibrate()

def local_calibration():
    condition_dictionary = {}
    cp_name = [100, 85, 75, 60]
    for cp in cp_list:
        for vin in vin_list:
            condition_dictionary[f'{cp_name[cp]}% {vin}Vac'] = ate_gui.get_coordinates_manual(f'{cp_name[cp]}% {vin}Vac')
    with open('cvcc_conditions_coordinates.txt', 'w') as f:
        f.write(str(condition_dictionary))
    return condition_dictionary

def load_local_calibration():
    with open('cvcc_conditions_coordinates.txt', 'r') as f:
        str_dict = f.read()
        condition_dictionary = eval(str_dict)
    return condition_dictionary

def calibration():
    # loading coordinates for the autogui
    if os.path.isfile('cvcc_conditions_coordinates.txt'): condition_dictionary = load_local_calibration()
    else: condition_dictionary = local_calibration()

    # asking the user if calibration is needed
    recalibrate_status = 0
    while recalibrate_status != 'y':
        recalibrate_status = input("Recalibrate? (y/n): ")
        if recalibrate_status == 'y': condition_dictionary = local_calibration()
        elif recalibrate_status == 'n': break

    return condition_dictionary

def cvcc(cp, vin, soak = 5, delay_per_line = 5, delay_per_load = 5):
    sleep(1)
    discharge_output()
    timer = 17*60

    ate_gui.cvcc(cp, vin)
    ate_gui.run_test()
    sleep(timer)
    sleep(15)

    print(f'{cp_name[cp]}% {vin}Vac >> completed')
    discharge_output()

def main():

    input("Make sure to change settings for Line/Load Regulation suited for your application.")

    condition_dictionary = calibration()

    # start automation
    ate_gui.alt_tab()
    ate_gui.esc()
    ate_gui.abort_test()

    cp_name = [100, 85, 75, 60]
    for cp in cp_list:
        for vin in vin_list:
            ate_gui.click(condition_dictionary[f'{cp_name[cp]}% {vin}Vac']) # select tab in excel
            cvcc(cp, vin, soak = 5, delay_per_line = 5, delay_per_load = 5)
    
    ate_gui.alt_tab()

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)