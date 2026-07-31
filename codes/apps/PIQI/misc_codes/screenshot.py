# from powi.equipment import Oscilloscope
# from filemanager import path_maker
# import os
# from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
# import getpass
# username = getpass.getuser().lower()
# import sys


##################################################################################
"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
import numpy as np
import shutil
import os
import pandas as pd

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
##################################################################################
scope_address = "10.125.10.101"
# scope_address = sys.argv[1]
filename = sys.argv[1]
test = filename
waveforms_folder = f'C:/Users/{username}/Desktop/Screenshots/{date}/'
path = path_maker(f'{waveforms_folder}')


scope = Oscilloscope(scope_address)
filename = f"{filename}.png"

def screenshot(filename, path):
    global waveform_counter

    scope.get_screenshot(filename, path)
    print(filename)
    waveform_counter += 1


def screenshot_looper(filename, path):
    iter = 0
    while "end" != input(">> Press ENTER to continue scope capture. Type 'end' to stop capturing: "):
        fname = filename.split('.png')[0] + f'_{iter}' + '.png'
        iter += 1
        screenshot(fname, path)

def main():

    screenshot(filename, path)
    # screenshot_looper(filename, path)




if __name__ == "__main__":
    # headers(test)
    main()
    # footers(waveform_counter)