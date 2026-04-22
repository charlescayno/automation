# set



"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
from filemanager import path_maker, remove_file
import winsound as ws
from playsound import playsound
waveform_counter = 0

from AUTOGUI_CONFIG import *
import os.path
from os import path

import shutil

##################################################################################

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.11.0"

"""USER INPUT"""
led_list = [30]
# led_list = convert_argv_to_int_list(sys.argv[1])

vin_list = [120,277]
# vin_list = [100]
# vin_list = convert_argv_to_int_list(sys.argv[2])

dim_list = [10,9,8,7,6,5,4,3,2,1.5,1.4,1.3,1.2,1.1,1,0.9,0.8,0.7,0.6,0.5,0]
# test_list = [1,2] # 1 - min to max, 2 - max to min
# test_list = convert_argv_to_int_list(sys.argv[3])

batch = input("Batch: ")
unit = input("Unit: ")
test = "Flicker"
waveforms_folder = f'C:/Users/ccayno/Desktop/DER/DER-935/2 Marketing Sample Units/Batch {batch}/Unit {unit}/{test}'


"""DO NOT EDIT BELOW THIS LINE"""
##################################################################################


"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
# pms = PowerMeter(source_power_meter_address)
# pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)

"""GENERIC FUNCTIONS"""

def discharge_output():
    ac.turn_off()
    for i in range(1,9):
        eload.channel[i].cc = 1
        eload.channel[i].turn_on()
        eload.channel[i].short_on()
    sleep(2)
    for i in range(1,9):
        eload.channel[i].turn_off()
        eload.channel[i].short_off()
    sleep(2)


ate_gui = AutoguiCalibrate()


def main():
    
    no_of_conditions = len(led_list)*len(vin_list)*len(dim_list)
    etc = 1*no_of_conditions

    print(f'Estimated time of completion is {etc} minutes')


    prompt("Press ENTER to start flicker test")
    
    

    ate_gui.click('select_ate_app')

    for LED in led_list:

        # tts(f"Change LED load to {LED} Volts.")

        for vin in vin_list:
            for dim in dim_list:
                
                ate_gui.initialize_analog_dimming(dim)
                ate_gui.ac_turn_on(vin)

                sleep(5)
                
                tts("Getting flicker")
                ate_gui.click('select_flicker_app')
                sleep(1)
                ate_gui.click('flicker_button')
                sleep(1)
                ate_gui.click('flicker_button')
                sleep(1)

                sleep(10)

                tts("Capturing screenshot")

                for i in range(10):
                    
                    image_file = f"{LED}V_{vin}Vac_{dim}V_{i+1}.png"
                    pyautogui.screenshot(image_file)

                    path = path_maker(f'{waveforms_folder}/{LED}V/Dim_{dim}V')
                    source = f'{os.getcwd()}/{image_file}'
                    destination = f'{path}/{image_file}'
                    remove_file(destination)
                    shutil.move(source, destination)
                    
                    sleep(0.2)

                ate_gui.click('select_file_tab')
                sleep(1)
                ate_gui.click('select_save_as')
                sleep(1)

                csv_file_name = f"{LED}V_{vin}Vac_{dim}V"
                print(csv_file_name)
                pyautogui.write(csv_file_name)
                sleep(1)
                
                ate_gui.enter()
                sleep(1)

                
                

                sleep(1)
                ate_gui.click('select_ate_app')
                sleep(1)
                ate_gui.ac_turn_off()
                

                discharge_output()
             

    

if __name__ == "__main__":
    
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)


