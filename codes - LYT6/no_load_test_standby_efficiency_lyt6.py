"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
import numpy as np

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl, Keithley_DC_2230G
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
from powi.equipment import excel_to_df, df_to_excel, image_to_excel, col_row_extractor, get_anchor
from powi.equipment import create_header_list, export_to_excel, export_screenshot_to_excel
from powi.equipment import path_maker, remove_file

import getpass
username = getpass.getuser().lower()

from datetime import datetime
now = datetime.now()
date = now.strftime('%m%d')

import shutil
import os
import pandas as pd




##################################################################################

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 30 
load_power_meter_address_1 = 10 
load_power_meter_address = 2
dimming_power_meter_address = 21
eload_address = 8
scope_address = "10.125.11.10"
dc_source_address = '4'

##################################################################################

vin_list = [90,100,110,115,120,132,180,200,230,265]
vout = 42
iout = 1
soak_time = 30 # s
integration_time = 60 # s


test = "No Load"
condition = input(">> Condition: ")
excel_name = f"{date} {condition}"
waveforms_folder = f'C:/Users/{username}/Desktop/Standby Efficiency at Open Load (DER-742)/{test}/'
path = path_maker(f'{waveforms_folder}')

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
pml1 = PowerMeter(load_power_meter_address_1)
eload = ElectronicLoad(eload_address)


"""DISCHARGE FUNCTION"""
def discharge_output(times=1):
    ac.turn_off()
    for i in range(times):
        for i in range(1,9):
            eload.channel[i].cc = 1
            eload.channel[i].turn_on()
            eload.channel[i].short_on()
        sleep(2)

        for i in range(1,9):
            eload.channel[i].turn_off()
            eload.channel[i].short_off()
        sleep(2)


def collect_data(vin):


    ################ SUBJECT TO CHANGE ################
    vaux = float(f"{pml1.voltage:.6f}")
    vac = vin
    freq = ac.set_freq(vin)
    vac_actual = float(f"{pms.voltage:.6f}")
    iin = float(f"{pms.current*1000:.6f}")
    pin = float(f"{pms.power:.6f}")
    pf = float(f"{pms.pf:.6f}")
    thd = float(f"{pms.thd:.6f}")
    vo1 = float(f"{pml.voltage:.6f}")
    io1 = float(f"{pml.current*1000:.6f}")
    po1 = float(f"{pml.power:.6f}")
    vreg1 = float(f"{100*(float(vo1)-vout)/float(vo1):.6f}")
    iout1 = (float(io1)/1000)
    try: ireg1 = float(f"{100*(iout1-iout)/iout1:.6f}")
    except: ireg1 = 0
    eff = float(f"{100*(float(po1))/float(pin):.6f}")

   
    output_list = [vac, freq, vac_actual, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff, vaux]

    return output_list


def operation():


    ################### COPY PASTE THIS CODE IN HEADER OF MAIN ###################
    df_header_list = ['Vin', 'Freq (Hz)', 'Vac (VAC)', 'Iin (mA)', 'Pin (W)', 'PF', 'THD (%)', 'Vo (V)', 'Io1 (mA)', 'Po (W)', 'Vreg (%)', 'Ireg (%)', 'Eff (%)', 'Vaux (V)'] 
    df = create_header_list(df_header_list)
    ##############################################################################

    eload.channel[5].cc = 0.0034
    eload.channel[5].turn_on()

    for vin in vin_list:

        ac.voltage = vin
        ac.turn_on()
    
        soak(soak_time)
        pms.integrate(integration_time)
        pml1.integrate(integration_time)
        soak(integration_time+5)

        output_list = collect_data(vin)
        export_to_excel(df, waveforms_folder, output_list, excel_name, sheet_name=f"{condition}", anchor="B2")
        print(df)

    print(f"\n\nFinal Data: ")
    print(df)

    discharge_output(2)
    pms.reset()
    pml.reset()
    pml1.reset()

    
def main():
    global waveform_counter
    discharge_output(1)
    operation()

        
if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
