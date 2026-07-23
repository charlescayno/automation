from functools import wraps
from math import isnan
from time import sleep, time
from abc import ABC, abstractmethod
import atexit
import os
import sys
import shutil
# try:
#     from pyfirmata import Arduino, util
#     import pyfirmata
#     import pyvisa
#     import numpy as np
#     from gtts import gTTS
#     from playsound import playsound

# except:
#     import pip
#     pip.main(['install','pyqt5'])
#     pip.main(['install','pyinstaller'])
#     pip.main(['install','pyautogui'])
#     pip.main(['install','pyfirmata'])
#     pip.main(['install', 'pyvisa'])
#     pip.main(['install','pandas'])
#     pip.main(['install','opencv-python'])
#     pip.main(['install','matplotlib'])
#     pip.main(['install','numpy'])
#     pip.main(['install', 'gTTS'])
#     pip.main(['install', 'playsound'])

#     from pyfirmata import Arduino, util
#     import pyfirmata
#     import pyvisa
#     import numpy as np

import pyvisa
import numpy as np

GPIB_NO = 0
PORT = 0

type_to_address = {
    'gpib': f'GPIB{GPIB_NO}',
    'lan': 'TCPIP',
    'usb': 'USB',
    'serial': 'ASRL'
    }

def reject_nan(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for _ in range(10):
            response = func(*args, **kwargs)
            if not isnan(response):
                return response
            sleep(0.2)
        return None
    return wrapped

class Equipment(ABC):
    def __init__(self, address, comm_type='gpib', timeout=10000):
        rm = pyvisa.ResourceManager()
        # print(rm.list_resources()) # print out devices connected on the VISA COM
        if comm_type == 'serial':
            self.address = f'{type_to_address[comm_type]}{address}'
            print(self.address)
        else:
            self.address = f'{type_to_address[comm_type]}::{address}'
        self.timeout = timeout
        try:
            self.device = rm.open_resource(self.address)
            self.device.timeout = self.timeout
            atexit.register(self.cleanup)
        except Exception as e:
            raise pyvisa.VisaIOError(e)
            
        self._id = 0

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                 '(address={self.address}, timeout={self.timeout})')

    @abstractmethod
    def cleanup(self):
        pass

    @property
    def id(self):
        self._id = self.write('*IDN?')
        return self._id

    def close(self):
        self.device.close()

    # def write(self, command):
    #     response = None
    #     try:
    #         if "?" in command:
    #             response = self.device.query(command).strip()
    #         else:
    #             self.device.write(command)
    #     except Exception as e:
    #         raise pyvisa.VisaIOError(e)

    #     return response
    
    def write(self, command):
        response = None
        reply_available = False # CDO
        try:
            if "BDMM" in command: # CDO
                reply_available = True
                command = command.split(':')[1]

            if "?" in command:
                response = self.device.query(command).strip()
            else:
                self.device.write(command)

            if reply_available: # CDO
                self.device.read()
                reply_available = False

        except Exception as e:
            raise pyvisa.VisaIOError(e)

        return response



# class Arduino(Equipment):

#     """UNDER DEVELOPMENT"""


#     def __init__(self, address, comm_type='serial', timeout=10000):
#         super().__init__(address, comm_type, timeout)
#         self.device.baud_rate = 115200
#         self.device.flow_control = 0
#         # self.device.write_termination = '\n'
#         # self.device.read_termination = '\n'
#         sleep(2)

#     def read(self):
#         print(self.device.read_raw())
#         # return self.device.read_raw().rstrip().decode('utf-8')

#     def cleanup(self):
#         self.close()


"""UNUSED CLASSES"""                 
class SignalGenerator(Equipment):
    def __init__(self, address, comm_type='usb', timeout=10000):
        super().__init__(address, comm_type, timeout)

    def cleanup(self):
        self.close()

class EMI(Equipment):
    def __init__(self, address, comm_type='lan', timeout=10000):
        super().__init__(address, comm_type, timeout)

    def cleanup(self):
        self.close()



"""CDO Classes"""
class Yokogawa_Oscilloscope_DLM5058(Equipment):
    def __init__(self, address, comm_type='lan', timeout=20000):
        super().__init__(address, comm_type, timeout)

 ##################### CH ON/OFF ###################    
    def channel_state(self, channel = 1, state ='ON'):
        self.write(f':CHAN{channel}:DISP {state}')

    def channel_state_all_off(self): 
        for channel in range(1, 9): 
            self.write(f':CHAN{channel}:DISP OFF')

 ##################### V&T /DIV #################### 
    
    def set_vdiv(self, channel = 1, vdiv = '1V'): #5mV to 100V
        self.write(f':CHAN{channel}:VDIV {vdiv}')

    def set_tdiv(self, tdiv = '10US'): #500ps to 500s
        self.write(f':TIM:TDIV {tdiv}')

 ##################### POSITION ####################

    def set_vert_position(self, channel = 1, vert_pos = 0): #-4div to 4div
        self.write(f':CHAN{channel}:POS {vert_pos}')

    def set_horiz_position(self, horiz_pos = 0): #Percentage 0% to 100%
        self.write(f':TRIG:POS {vert_pos}')

 ##################### ATTENUATION #################

    def set_probe_attenuation(self, channel = 1, attenuation = 10): #Add C{attenuation} if current
        self.write(f':CHAN{channel}:PROBE {attenuation}')

 ##################### TRIGGER #####################

    def set_trigger_mode(self, trig_mode = 'NORM'): #AUTO, NORMal, A(uto)LEVel, NSINgle
        self.write(f':TRIG:MODE {trig_mode}')

    def set_trigger_level(self, channel = 1, trig_lev = '1V'): 
        self.write(f':TRIG:SOUR:CHAN{channel}:LEV {trig_lev}')

 ##################### MEASURE #####################

    def disp_meas_off(self, channel = 1): 
        self.write(f':MEAS:CHAN{channel}:ALL OFF')

    def disp_meas_off_all(self): 
        for channel in range(1, 9): 
            self.write(f':MEAS:CHAN{channel}:ALL OFF')

    def disp_meas(self, channel = 1, parameter = 'FREQ'): 
        self.write(f':MEAS:CHAN{channel}:{parameter}:STATE ON') 
        ''' List of Parameters Drop-Down
            AMPLitude
            AVERage
            AVGFreq
            AVGPeriod
            BWIDth
            DELay
            DT
            DUTYcycle
            ENUMber
            FALL
            FREQuency
            HIGH
            LOW
            MAXimum
            MINimum
            NOVershoot
            NWIDth
            PERiod
            PNUMber
            POVershoot
            PTOPeak
            PWIDth
            RISE
            RMS
            SDEViation
            TY1Integ
            TY2Integ
            V1
            V2'''

    def get_meas_value(self, channel = 1, parameter = 'FREQ'):
        sleep(0.05) 
        result = self.write(f':MEAS:CHAN{channel}:{parameter}:VAL?').split(' ')[1]
        return result 

    def disp_meas_statistics(self, mode = 'CONT'): #OFF|ON|CONTinuous|CYCLe|HISTory
        self.write(f':MEAS:MODE {mode}')

    def set_sample_count(self, count = 1000): 
        self.write(f':ACQ:COUNT {count}')
        self.write(f':TRIG:MODE NORM')
        status = int(self.write(f':STATus:CONDition?'))
        while status > 0:
            status = int(self.write(f':STATus:CONDition?'))

    def get_min_mean_max_sd(self, channel = 1, parameter = 'FREQ'):
        result = {
            "maximum": self.write(f':MEASure:CHANnel{channel}:{parameter}:MAXimum?').split(' ')[1],
            "mean": self.write(f':MEASure:CHANnel{channel}:{parameter}:MEAN?').split(' ')[1],
            "minimum": self.write(f':MEASure:CHANnel{channel}:{parameter}:MINimum?').split(' ')[1],
            "sdeviation": self.write(f':MEASure:CHANnel{channel}:{parameter}:SDEViation?').split(' ')[1]
        }
        return result

 ##################### SCREENSHOT ###################
    def set_drive(self, drive = 'USB'): #FLAShmem|NETWork|USB 
        self.write(f' :IMAGE:SAVE:DRIVE {drive}')
    
    def set_background(self, background = 'GRAY'): #COLor|GRAY|OFF|REVerse 
        self.write(f' :IMAGE:TONE {background}')

    def set_filename(self,temperature = '25', test_id = ' ', condition = '5V_25V'): 
        self.write(f' :IMAGE:SAVE:NAME "{temperature}C_{test_id}_{condition}_"')

    def screenshot(self): 
        self.write(f' :IMAGE:EXECUTE')
    
 ##################### CLOSE ########################
    def stop(self):
        self.write(':STOP')

    def cleanup(self):
        self.close()

class Tektronix_SigGen_AFG31000(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=20000):
        super().__init__(address, comm_type, timeout)

 ##################### CH ON/OFF ###################    
    def channel_state(self, channel = 1, state ='ON'):
        self.write(f':OUTP{channel}:STAT {state}')

    def channel_state_all_off(self): 
        for channel in range(1, 3): 
            self.write(f':OUTP{channel}:STAT OFF')

    def set_load_impedance(self, channel = 1, impedance = 'INF'): 
        self.write(f':OUTP{channel}:IMPedance {impedance}')

 ##################### CONTINUOUS ###################
    def out_cont_sine(self, channel = 1, frequency = '10kHz', phase = '0 DEG', low = '-500mV', high = '500mV', units = 'VPP'): 
        self.write(f' :SOURce{channel}:FUNCtion:SHAPe SIN')
        self.write(f' :SOURce{channel}:FREQuency:FIXed {frequency}')
        self.write(f' :SOURce{channel}:PHASe:ADJust {phase}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:LOW {low}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:HIGH {high}')
        self.write(f' :SOURce{channel}:VOLTage:UNIT {units}')

    def out_cont_square(self, channel = 1, frequency = '10kHz', phase = '0 DEG', low = '-500mV', high = '500mV', units = 'VPP'): 
        self.write(f' :SOURce{channel}:FUNCtion:SHAPe SQU')
        self.write(f' :SOURce{channel}:FREQuency:FIXed {frequency}')
        self.write(f' :SOURce{channel}:PHASe:ADJust {phase}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:LOW {low}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:HIGH {high}')
        self.write(f' :SOURce{channel}:VOLTage:UNIT {units}')

    def out_cont_ramp(self, channel = 1, frequency = '10kHz', phase = '0 DEG', low = '-500mV', high = '500mV', units = 'VPP', symmetry = 50.0): 
        self.write(f' :SOURce{channel}:FUNCtion:SHAPe RAMP')
        self.write(f' :SOURce{channel}:FREQuency:FIXed {frequency}')
        self.write(f' :SOURce{channel}:PHASe:ADJust {phase}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:LOW {low}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:HIGH {high}')
        self.write(f' :SOURce{channel}:VOLTage:UNIT {units}')
        self.write(f' :SOURce{channel}:FUNCtion:RAMP:SYMMetry {symmetry}')              

    def out_cont_pulse(self, channel = 1, frequency = '10kHz', phase = '0 DEG', low = '-500mV', high = '500mV', units = 'VPP', duty = 999, width = 'ABC'): #Choose duty or width
        self.write(f' :SOURce{channel}:FUNCtion:SHAPe PULSE')
        self.write(f' :SOURce{channel}:FREQuency:FIXed {frequency}')
        self.write(f' :SOURce{channel}:PHASe:ADJust {phase}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:LOW {low}')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:HIGH {high}')
        self.write(f' :SOURce{channel}:VOLTage:UNIT {units}')
        
        if (duty != 999):
            self.write(f' :SOURce{channel}:PULSe:DCYCle {duty}')
            # print(duty)
        if (width != 'ABC'):
            self.write(f' :SOURce{channel}:PULSe:WIDTh {width}')
            print(width)
                
    def out_DC(self, channel = 1, voltage = '5V'): 
        self.write(f' :SOURce{channel}:FUNCtion:SHAPe DC')
        self.write(f' :SOURce{channel}:VOLTage:LEVel:IMMediate:OFFSet {voltage}')

 ##################### CLOSE ########################
    def stop(self):
        self.write(':STOP')

    def cleanup(self):
        self.close()

class Keithley_DC_2230G(Equipment):
    def __init__(self, address, comm_type='gpib', timeout=20000):
        super().__init__(address, comm_type, timeout)

 #################### SET VOL&CURR #################
    def set_volt_curr(self, channel ='CH1', voltage = 0.0, current = 0.0):
        self.write(f'APPL {channel}, {voltage}, {current}')
        

    def channel_state(self, channel ='CH1', state = 'ON'): #Individual
        self.write(f'INST {channel}')  
        self.write(f'CHAN:OUTP {state}')

    def channel_state_all(self, state = 'ON'): #For all channels
        self.write(f'OUTP {state}')          

 #################### CLOSE ########################
    def stop(self):
        self.write(':STOP')

    def cleanup(self):
        self.close()

class Fluke_BDMM_8808A(Equipment):
    def __init__(self, address, comm_type='serial', timeout=20000):
        super().__init__(address, comm_type, timeout)

 #################### BDMM #################
    def remote_mode(self):
        self.write(f'BDMM:REMS')
        

    def set_func(self, function = 'VDC'): #VDC, VAC, AAC, ADC, OHMS, CONTinuity, DIODE, FREQ
        self.write(f'BDMM:{function}')
        sleep(5)

    def get_meas_value(self):
        return self.write(f'BDMM:VAL?')

    def meas_hold(self):
        return self.write(f'BDMM:HOLD')

 #################### CLOSE ########################
    def stop(self):
        self.write(':STOP')

    def cleanup(self):
        self.close()


"""Charles' Custom Functions"""

# initialize variables
global Iout_index
global waveform_counter
global start
global waveforms_folder
waveform_counter = 0
Iout_index = 0
from datetime import datetime



import os
import shutil

def path_maker(file_path: str):
    """
        file_path: Enter the file path you want to create

        returns the string value of new path created
    """

    folder_list = file_path.split('/')

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


def remove_file(file_path: str):
    """
        file_path: Enter the file path you want to delete

        returns the string value of new path created
    """

    if os.path.exists(file_path): os.remove(file_path)


def move_file(source_path: str, destination_path: str):
    """
        source_path : path/file
        destination_path : path/file
    """
    source = f'{source_path}'
    destination = f'{destination_path}'
    remove_file(destination)
    shutil.move(source, destination)











def headers(test_name):
    global start
    print()
    print("="*80)
    print(f"Test: {test_name}")
    create_folder(test_name)
    start = datetime.now()
    print("="*80)

def create_folder(test_name):
    if not os.path.exists('waveforms'): os.mkdir('waveforms')
    waveforms_folder = f'waveforms/{test_name}'
    pathname = f"{os.getcwd()}/{waveforms_folder}"
    if not os.path.exists(pathname): os.mkdir(pathname)

def sfx():
    import winsound as ws
    ws.PlaySound("dingding.wav", ws.SND_ASYNC)
    sleep(2)  

def footers(waveform_counter):

    # from playsound import playsound
    # import winsound as ws
    # # playsound("test_complete.mp3")

    print("="*80)
    if waveform_counter > 0: print(f'{waveform_counter} waveforms captured.')
    print('test complete.')
    print()
    end = datetime.now()
    total_time = end-start
    temp = ""
    
    print(f"START TIME: {temp:>12}{start}")
    print(f"COMPLETION TIME: {temp:>7}{end}")
    print(f"TOTAL TESTING TIME: {temp:>16}{total_time}")
    print("="*80)
    
    sfx()    
    
def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")

def convert_argv_to_int_list(a=[]):
    str_list = a.strip('[]').split(',')
    int_list = [int(x) for x in str_list]
    return int_list

def convert_argv_to_str_list(a=[]):
    str_list = a.strip('[]').split(',')
    return str_list

# class LEDControl():

#     """
#     CLASS FUNCTION TO CONTROL LED LOADS
    
#     """


#     def __init__(self):

#         from time import sleep, time
#         import serial.tools.list_ports
#         import math
#         from pyfirmata import Arduino, util
#         import pyfirmata

#         # automatic detection of comm port
#         ports = serial.tools.list_ports.comports()
        
#         commPort = 'None'
#         for i in range(0, len(ports)):

#             port = str(ports[i])
#             if 'USB Serial Device' in port:
#                 commPort = port[3:5]
                
        
#         if commPort != 'None':
#             try:
#                 # print(commPort)
#                 self.board = pyfirmata.Arduino(f'COM{commPort}')
#                 self.iterator = util.Iterator(self.board)
#                 self.iterator.start()
#                 print(f'LED Load Control: Connected to COM{commPort}')
#                 self.initialize_relays()
#             except Exception as e:
#                 raise e
#         else:
#             raise ValueError


#     def initialize_relays(self):
#         self.RELAY1 = self.board.get_pin('d:10:o')
#         self.RELAY2 = self.board.get_pin('d:9:o')
#         self.RELAY3 = self.board.get_pin('d:8:o')

#     def voltage(self, voltage: int):
#         if voltage >= 41:
#             self.RELAY1.write(1)
#             self.RELAY2.write(0)
#             self.RELAY3.write(0)
#             print(f"LED set to {voltage}V.")
#         elif voltage > 24 and voltage < 40:
#             self.RELAY1.write(0)
#             self.RELAY2.write(1)
#             self.RELAY3.write(0)
#             print(f"LED set to {voltage}V.")
#         elif voltage <= 24 and voltage > 0:
#             self.RELAY1.write(0)
#             self.RELAY2.write(0)
#             self.RELAY3.write(1)
#             print(f"LED set to {voltage}V.")
#         elif voltage == 0:
#             self.RELAY1.write(0)
#             self.RELAY2.write(0)
#             self.RELAY3.write(0)
#             print(f"LED set to NL.")
#         else: print("Invalid LED.")

# def tts(message):
#     language = 'fr'
#     myobj = gTTS(text=message, lang=language, slow=False)
#     path_maker(f'{os.getcwd()}/sfx')
#     if not os.path.exists(f"{os.getcwd()}/sfx/{message}.mp3"):
#         myobj.save(f"{message}.mp3")
#         move_file(f"{message}.mp3", f"{os.getcwd()}/sfx/{message}.mp3")
#     playsound(f"{os.getcwd()}/sfx/{message}.mp3")
#     print(f"{message}")

# def prompt(message):
#     language = 'en'
#     myobj = gTTS(text=message, lang=language, slow=False)
#     path_maker(f'{os.getcwd()}/sfx')
#     if not os.path.exists(f"{os.getcwd()}/sfx/{message}.mp3"):
#         myobj.save(f"{message}.mp3")
#         move_file(f"{message}.mp3", f"{os.getcwd()}/sfx/{message}.mp3")
#     playsound(f"{os.getcwd()}/sfx/{message}.mp3")
#     input(f"{message}")









# import pandas as pd
# from openpyxl import Workbook
# import openpyxl
# from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
# from openpyxl.utils import get_column_letter
# import os
# import matplotlib.pyplot as plt

# def get_anchor(col, row):
#     """
#     get anchor given a numerical col row  -> (col = 2, row = 4 -> 'B4')
#     returns anchor (str)
#     """
#     anchor = f"{get_column_letter(col)}{row}"
#     return anchor

# def col_row_extractor(excel_coordinate):
#     """
#     extract col and row given an excel coordinate (i.e. 'B4' -> col = 2, row = 4)

#     excel_coordinate : i.e. 'B4' (str)
#     returns col, row (int)
#     """
#     coordinates = coordinate_from_string(excel_coordinate)
#     col = column_index_from_string(coordinates[0])
#     row = coordinates[1]
#     return col, row

# def excel_to_df(filename, sheet_name, start_corner, end_corner):
#     """
#     reading dataframe from excel.
    
#     filename     : must include full filename path (cwd + path + file.extension)
#     sheet_name   : sheet name in excel file
#     start_corner : cell coordinate to start selection of data
#     end_corner   : cell coordinate to end selection of data

#     returns df
#     """

#     # print(f"reading dataframe from {filename} {sheet_name}")

#     start_col, start_row = col_row_extractor(start_corner)
#     end_col, end_row = col_row_extractor(end_corner)

#     skiprows = start_row - 2
#     usecols = f'{get_column_letter(start_col)}:{get_column_letter(end_col)}'
#     nrows = end_row - start_row + 1

#     return pd.read_excel(filename, sheet_name, skiprows=skiprows, usecols=usecols, nrows=nrows)
#     # return pd.read_csv(filename, sheet_name, skiprows=skiprows, usecols=usecols, nrows=nrows)

# def df_to_excel(wb, sheet_name, df, anchor):
#     """
#     writing dataframe to excel.

#     wb          : workbook
#     sheet_name  : sheet name in excel file
#     df          : dataframe
#     anchor      : anchor point in excel

#     returns None
#     """



#     sheet_list = wb.get_sheet_names()
#     if sheet_name not in sheet_list: wb.create_sheet(sheet_name)
#     try:
#         default_sheet = wb.get_sheet_by_name('Sheet1')
#         # wb.remove_sheet(default_sheet) 
#     except: pass


#     start_col, start_row = col_row_extractor(anchor)
#     df_row_len, df_col_len = df.shape
#     end_row = start_row + df_row_len - 1
#     end_col = start_col + df_col_len - 1

#     for row in range(start_row, end_row+1):
#         for col in range(start_col, end_col+1):
#             wb[sheet_name][f'{get_column_letter(col)}{row}'] = df.iloc[row-start_row, col-start_col]

# def image_to_excel(wb, sheet_name, filename, folder_path, anchor):
#     """
#     writing image to excel.

#     image size -> 39 rows, 16 columns
#     wb          : workbook
#     sheet_name  : sheet name in excel file
#     filename    : filename of theh image
#     folder_path : image location
#     anchor      : anchor point in excel
#     """

#     file = folder_path + filename
#     # file = os.getcwd() + folder_path + filename
#     img = openpyxl.drawing.image.Image(file)
#     img.anchor = anchor
#     img.width = 1056
#     img.height = 659.90551181

#     sheet_list = wb.get_sheet_names()
#     if sheet_name not in sheet_list: wb.create_sheet(sheet_name)
#     try:
#         default_sheet = wb.get_sheet_by_name('Sheet1')
#         wb.remove_sheet(default_sheet)
#     except: pass

#     col, row = col_row_extractor(anchor)
#     wb[sheet_name][f'{get_column_letter(col)}{row-1}'] = filename
#     wb[sheet_name].add_image(img)





# #################### DATA EXPORT CODE ###########################################################
# def create_header_list(df_header_list):
#     df = pd.DataFrame(columns = df_header_list)
#     df.loc[len(df)] = df_header_list
#     print(df)
#     return df

# def export_to_excel(df, waveforms_folder, output_list, excel_name, sheet_name, anchor):
#     df.loc[len(df)] = output_list
#     print(output_list)

#     src = f"{os.getcwd()}/blank.xlsx"
#     dst = f"{waveforms_folder}/{excel_name}.xlsx"
#     if not os.path.exists(dst): shutil.copyfile(src, dst)

#     wb = load_workbook(dst)
#     df_to_excel(wb, sheet_name, df, anchor)
#     wb.save(dst)

# def export_screenshot_to_excel(excel_name, waveforms_folder, sheet_name, filename, anchor):

#     src = f"{os.getcwd()}/blank.xlsx"
#     dst = f"{waveforms_folder}/{excel_name}.xlsx"
#     if not os.path.exists(dst): shutil.copyfile(src, dst)

#     wb = load_workbook(dst)
#     image_to_excel(wb, sheet_name, filename=filename, folder_path=waveforms_folder, anchor=anchor)
#     wb.save(dst)


























# from openpyxl import Workbook, load_workbook
# from openpyxl.chart import ScatterChart, Reference, Series

# def create_scatter_chart(title="Efficiency (%)", style=2, x_title='Input Voltage (VAC)', y_title='Efficiency (%)',
#                         x_min_scale = 90, x_max_scale = 277, x_major_unit = 20, x_minor_unit = 10,
#                         y_min_scale = 0, y_max_scale = 100, y_major_unit = 10, y_minor_unit = 5):
 

#     chart = ScatterChart()
#     chart.title = title
#     chart.style = style
#     chart.x_axis.title = x_title
#     chart.y_axis.title = y_title
#     chart.height = 10 # default is 7.5
#     chart.width = 20 # default is 15

#     chart.x_axis.scaling.min = x_min_scale
#     chart.x_axis.scaling.max = x_max_scale
#     chart.y_axis.scaling.min = y_min_scale
#     chart.y_axis.scaling.max = y_max_scale

#     chart.x_axis.majorUnit = x_major_unit
#     chart.x_axis.minorUnit = x_minor_unit
#     chart.y_axis.majorUnit = y_major_unit
#     chart.y_axis.minorUnit = y_minor_unit


#     return chart

# def reset_chartsheet(wb):
#     chart_sheet = wb["Chart"]
#     try:
#         no_of_existing_charts = len(chart_sheet._charts)
#         for i in range(no_of_existing_charts):
#             del chart_sheet._charts[(i-1)]
#     except: pass
    
#     return chart_sheet

# def save_chartsheet(chart_sheet, chart, chart_position):
#     chart_sheet.add_chart(chart, chart_position)

# def append_series(path, wb, ws_name, x_anchor, last_row_anchor, series_title, chart):
#     ## used in der-727_chart_compiler.py
    
#     df = excel_to_df(path, ws_name, x_anchor, last_row_anchor)
#     ws = wb[ws_name]
#     xcol, xrow = col_row_extractor(x_anchor)
#     last_col, last_row = col_row_extractor(last_row_anchor)
#     xvalues = Reference(ws, min_col=xcol, min_row=xrow, max_row=last_row)
#     values = Reference(ws, min_col=last_col, min_row=xrow, max_row=last_row)
#     series = Series(values, xvalues, title=series_title)
#     series.marker=openpyxl.chart.marker.Marker('auto')
#     series.graphicalProperties.line.noFill=False
#     chart.series.append(series) 
















if __name__ == '__main__':
    pass


