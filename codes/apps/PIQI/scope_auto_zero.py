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
# source_power_meter_address = 30 
# load_power_meter_address = 2
# pms = PowerMeter(source_power_meter_address)
# pml = PowerMeter(load_power_meter_address)
scope = Oscilloscope(scope_address)


def main():
    # pms.reset()
    # pml.reset()
    scope.time_scale(0.1)
    scope.auto_zero(1)
    scope.auto_zero(2)
    scope.auto_zero(3)
    scope.auto_zero(4)
    scope.display_intensity()
    scope.trigger_mode("AUTO")
    scope.run()

if __name__ == "__main__":
    main()
