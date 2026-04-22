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

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
pml1 = PowerMeter(load_power_meter_address_1)
eload = ElectronicLoad(eload_address)


def operation():

    ac.voltage = 2


    
def main():
    operation()

        
if __name__ == "__main__":

    main()
