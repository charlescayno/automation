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

from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
from powi.equipment import excel_to_df, df_to_excel, image_to_excel, col_row_extractor, get_anchor
from powi.equipment import create_header_list, export_to_excel, export_screenshot_to_excel
from powi.equipment import path_maker, remove_file, start_timer, end_timer
from misc_codes.equipment_settings import *

import getpass
username = getpass.getuser().lower()

from datetime import datetime
now = datetime.now()
date = now.strftime('%m%d')
##################################################################################


class GENERAL_CONSTANTS():

    DEFAULT_WIDE_RANGE_VIN_LIST = [90,100,110,115,120,132,180,200,230,265,277,300]
    PPT_VIN_LIST = [90,115,230,265,277,300]

    SOAK_TIME_PER_LINE_QUICK_CHECK = 1
    SOAK_TIME_PER_LINE_DER = 300

    HEADER_LIST_CC_LOAD = ['Vin', 'Freq (Hz)', 'Vac (VAC)', 'Iin (mA)', 'Pin (W)', 'PF', 'THD (%)', 'Vo (V)', 'Io1 (mA)', 'Po (W)', 'Vreg (%)', 'Ireg (%)', 'Eff (%)']
    HEADER_LIST_LED_LOAD = ['LED (V)','Vin', 'Freq (Hz)', 'Vac (VAC)', 'Iin (mA)', 'Pin (W)', 'PF', 'THD (%)', 'Vo (V)', 'Io1 (mA)', 'Po (W)', 'Vreg (%)', 'Ireg (%)', 'Eff (%)'] 




class GENERAL_FUNCTIONS():

    def CREATE_PATH(self, project, test):
        waveforms_folder = f'C:/Users/{username}/Desktop/{project}/{date}/{test}/'
        path = path_maker(f'{waveforms_folder}')
        return waveforms_folder

    def CREATE_DF_WITH_HEADER(self, header_list):
        """
            creates a data frame with empty header_list specified by user

            returns a dataframe
        """
        return create_header_list(header_list)

    def PRINT_FINAL_DATA_DF(self, df):
        print(f"\n\nFinal Data: ")
        print(df)

    def ESTIMATED_TEST_TIME(self, estimated_time):
        print(f"Estimated Testing Time: {round(math.ceil(estimated_time/60), 2)} mins.")

    
