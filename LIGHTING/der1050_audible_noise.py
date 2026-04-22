from xml.sax.handler import feature_external_ges
from powi.equipment import Keithley_DC_2230G
import pyautogui
from time import sleep, time
import pandas as pd
import os
import shutil
import numpy as np
# C:\Users\API\Anaconda3\Lib\site-packages\powi
# C:\Users\API\Desktop\Audible Automation\
#########################################################################################
"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
import numpy as np
import shutil
import os
import pandas as pd
import pyautogui

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl, Keithley_DC_2230G, Tektronix_SigGen_AFG31000
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
from powi.equipment import excel_to_df, df_to_excel, image_to_excel, col_row_extractor, get_anchor
from powi.equipment import create_header_list, export_to_excel, export_screenshot_to_excel
from powi.equipment import path_maker, remove_file

import getpass
username = getpass.getuser().lower()

from datetime import datetime
now = datetime.now()
date = now.strftime('%m%d')

import warnings

#########################################################################################
"""COMMS"""
ac_source_address = 5
source_power_meter_address = 30 
load_power_meter_address = 6
eload_address = 8
eload_channel = 5
sig_gen_address = 11
#########################################################################################
test = "Audible Noise using E-load"
print(test)
#########################################################################################
#########################################################################################
"""USER INPUTS"""
project = "DER-1050 Unit 1"
condition = "Audible Noise"
vin_list = [230]
vout = 5
iout = 0.5
#########################################################################################
#########################################################################################

percent_list_100_75 = range(100, 74, -1) # 100% to 75% loading
percent_list_75_50 = range(75, 49, -1) # 75% to 50% loading
percent_list_50_25 = range(50, 24, -1) # 50% to 25% loading
percent_list_25_0 = range(25, 0, -1) # 25% to 0% loading
#########################################################################################
ac_source = ACSource(ac_source_address)
eload = ElectronicLoad(eload_address)
sig_gen = Tektronix_SigGen_AFG31000(sig_gen_address)
#########################################################################################

def exists(filename):
    return os.path.isfile(filename)

def get_file_size(filename):
    if exists():        
        statinfo = os.stat(filename)
        return statinfo.st_size
    return 0

def file_to_df(filename, column_name):
    df = pd.read_excel(filename, skiprows=3)
    df.set_index('Hz', inplace=True)
    df.index.name = 'Frequency'
    df.columns = [column_name]
    return df

def append_df_to_file(filename, df):
    if exists(filename):
        base_df = pd.read_excel(filename, index_col=0, engine="openpyxl")
        base_df = pd.concat([base_df, df], axis=1)
    else:
        base_df = df
    base_df.to_excel(filename)

def copy_file(src, dst):
    shutil.copyfile(src, dst)

def delete_file(filename):
    try:
        os.remove(filename)
    except:
        pass

def path_maker(file_path: str):
    folder_list = file_path.split("/")
    new_path = ' '
    for i in folder_list:
        if new_path == ' ':
            path = f'{i}/'
        else:
            path = new_path + f'{i}/'
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        new_path = path
    return new_path

def cursor_move_click(button_position):
    sleep(2)
    pyautogui.moveTo(button_position)
    sleep(2)
    pyautogui.click()

def audible_noise_capture(percent, vin, duty):

    cc = iout*percent/100 if percent != 0 else 0
    print(vin, percent, cc)
    if cc == 0:
        eload.channel[eload_channel].turn_off()
    else:
        eload.channel[eload_channel].cc = cc
        eload.channel[eload_channel].turn_on()

    sleep(5)

    cursor_move_click(button_position_start)
    
    sleep(10)
    done = 0
    while not done:
        popout = pyautogui.locateOnScreen('Cancel.png')
        if not popout:
            sleep(10)
            break 

    image = pyautogui.screenshot(region=(pos1[0],pos1[1],pos2[0]-pos1[0],pos2[1]-pos1[1]))
    filename = f"{vin}Vac, 36V_duty_{duty}%_10kHz, {vout}V_{percent}% Load_{cc}A, {condition}.png"
    path1 = f"c/Users/API/Documents/{project}/screenshots/{condition}/specific loading"
    path1 = path_maker(path1)
    image.save(f"{path1}{filename}")
    print(filename)

def audible_noise_capture_final(vin, percent_batch, duty):
    image = pyautogui.screenshot(region=(pos1[0],pos1[1],pos2[0]-pos1[0],pos2[1]-pos1[1]))
    filename = f"{vin}Vac, 36V_duty_{duty}%_10kHz, {vout}V_{percent_batch}% Load, {condition}.png"
    path2 = f"c:/Users/API/Documents/{project}/screenshots/{condition}/batch loading"
    path2 = path_maker(path2)
    image.save(f"{path2}{filename}")
    print(filename)

def reset_chart():
    cursor_move_click(button_position_sequence)
    
    sleep(10)
    done = 0
    while not done:
        popout = pyautogui.locateOnScreen('Cancel.png')
        if not popout: break 

def AC_TURN_ON(voltage, type='AC'):
        ac_source.voltage = voltage
        ac_source.coupling = type
        ac_source.turn_on()

def SIG_GEN(duty):
    sig_gen.set_load_impedance(channel = 1, impedance = 'INF') 
    sig_gen.out_cont_pulse(channel = 1, frequency = 10000, phase = '0 DEG', low = '0V', high = '3.3V', units = 'VPP', duty = duty, width = 'ABC')
    sig_gen.channel_state(channel = 1, state ='ON')
    print(f"Duty = {duty}, Fsw = 10 kHz")
    soak(1)

def DISCHARGE_OUTPUT(times):    
    print("Discharging output..")
    ac_source.turn_off()
    for i in range(times):
        for i in range(1,9):
            # eload.channel[i].cr = 100
            eload.channel[i].short_on()
            eload.channel[i].turn_on()
        sleep(0.5)

        for i in range(1,9):
            eload.channel[i].turn_off()
            eload.channel[i].short_off()
        sleep(0.5)

def main():

    path_maker(f"c:/Users/API\Documents/{project}/screenshots/")

    # input(">>input upper left anchor. press enter to get coordinates.")
    # pos1 = pyautogui.position()
    # print(pos1)
    # input(">>input lower right anchor. press enter to get coordinates.")
    # pos2 = pyautogui.position()
    # print(pos2)
    # input(">> Exit checking..")


    global button_position_sequence, button_position_start
    global pos1
    global pos2

    pos1 = [598, 131]
    pos2 = [1365,607]
    button_position_sequence = (30, 135) # per load
    button_position_start = (360, 120) # by batch

    warnings.simplefilter("ignore")
    start = time()

    for vin in vin_list:

        duty_list = range(0, 110, 10)

        for duty in duty_list:
            
            DISCHARGE_OUTPUT(3)
            

            # GETTING NOISE FLOOR SCREENSHOT
            reset_chart()
            image = pyautogui.screenshot(region=(pos1[0],pos1[1],pos2[0]-pos1[0],pos2[1]-pos1[1]))
            image.save(f"c:/Users/API\Documents/{project}/screenshots/{vin}Vac, {vout}V, Noise Floor, {condition}.png")
            print(f"{vin}Vac, {vout}V, Noise Floor, {condition}.png")

            input(f">> Set input to {vin} Vac and output to {iout}A.")

            SIG_GEN(duty, 10000)

            AC_TURN_ON(vin)

            reset_chart()
            for percent in percent_list_100_75:
                audible_noise_capture(percent, vin, duty)
                audible_noise_capture_final(vin, "100-75", duty)

            # reset_chart()
            # for percent in percent_list_75_50:
            #     audible_noise_capture(percent, vin, duty)
            #     audible_noise_capture_final(vin, "75-50", duty)

            # reset_chart()
            # for percent in percent_list_50_25:
            #     audible_noise_capture(percent, vin, duty)
            #     audible_noise_capture_final(vin, "50-25", duty)
            
            # reset_chart()
            # for percent in percent_list_25_0:
            #     audible_noise_capture(percent, vin, duty)
            #     audible_noise_capture_final(vin, "25-0", duty)

            DISCHARGE_OUTPUT(3)
            
    end = time()
    print(f'Elapsed: {end-start} s')

        
if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
