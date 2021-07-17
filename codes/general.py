
"""IMPORT DEPENDENCIES"""
import sys
import pyautogui
from time import sleep, time
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
from powi.equipment import *
from time import sleep, time
import os
# import cv2
# waveform_counter = 0

# """INITIALIZE EQUIPMENT"""


# print("Intialize equipment.")
# ac = ACSource(ac_source_address)
# eload = ElectronicLoad(eload_address)
# scope = Oscilloscope(scope_address)
# # pms = PowerMeter(source_power_meter_address)
# # pml = PowerMeter(load_power_meter_address)

class Initialize():

    def __init__(self):
        import os.path
        from os import path
        
        if os.path.isfile('comm_address.txt'):
            self.calibration_status = True
        else:
            self.calibration_status = False
            

            self.save_settings()

    def initialize_variables(self):
        self.comm_address = {}

    def calibrate(self):
        self.initialize_variables()
        self.comm_address["ac_source_address"] = input("Enter AC SOURCE Address: ")
        self.comm_address["eload_address"] = input("Enter ELOAD Address: ")
        self.comm_address["scope_address"] = input("Enter SCOPE Address: ")
        self.comm_address["source_power_meter_address"] = input("SOURCE POWER METER Address: ")
        self.comm_address["load_power_meter_address"] = input("LOAD POWER METER Address: ")
    
    def save_settings(self):
        if self.calibration_status == False:
            self.calibrate()
            with open('comm_address.txt', 'w') as f:
                f.write(str(self.comm_address))
    
    def load_settings(self):
        with open('comm_address.txt', 'r') as f:
            str_dict = f.read()
            self.comm_address = eval(str_dict)
            return self.comm_address

    def recalibrate(self):
        print("Recalibrating...")
        self.calibration_status = False
        self.save_settings()
        print("Recalibration complete.")

    def Equipment(self):
        self.comm_address = self.load_settings()
        # self.ac = ACSource(self.comm_address["ac_source_address"])
