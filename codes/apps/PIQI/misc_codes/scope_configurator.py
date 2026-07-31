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

from datetime import datetime
now = datetime.now()
date = now.strftime('%Y_%m_%d')	

##################################################################################

"""COMMS"""

scope_address = "10.125.11.10"

"""DO NOT EDIT BELOW THIS LINE"""
##################################################################################

"""EQUIPMENT INITIALIZE"""

scope = Oscilloscope(scope_address)


def scope_settings():
    global condition
    
    scope.channel_settings(state='ON', channel=1, scale=0.4, position=-4, label="Vfb",
                            color='YELLOW', rel_x_position=20, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='OFF', channel=2, scale=2, position=-4, label="VDS",
                            color='PINK', rel_x_position=40, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='ON', channel=3, scale=2, position=-4, label="Vaux",
                            color='ORANGE', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    scope.channel_settings(state='ON', channel=4, scale=10, position=-4, label="Vout",
                            color='LIGHT_BLUE', rel_x_position=80, bandwidth=20, coupling='DCLimit', offset=0)
    
    
    
    scope.measure(1, "MAX,RMS")
    # scope.measure(2, "MAX,RMS")
    scope.measure(3, "MAX,RMS")
    scope.measure(4, "MAX,RMS")

    scope.time_position(10)
    
    scope.record_length(50E6)
    
    scope.time_scale(1)

    # scope.remove_zoom()
    # scope.add_zoom(rel_pos=21.727, rel_scale=1)
    
    trigger_channel = 1
    trigger_level = 1
    trigger_edge = 'POS'
    scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)

    scope.stop()



def main():

    scope_settings()
        
if __name__ == "__main__":

    main()
