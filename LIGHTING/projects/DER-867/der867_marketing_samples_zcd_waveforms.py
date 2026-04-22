import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from misc_codes.scope_settings_der867_zcd import *
from misc_codes.scope_setter import *

########################################## USER INPUT ##########################################
unit = 1
vin_list = [230]
load_type = 2

# PROJECT DETAILS
project = "DER-867"
excel_name = f"Unit {unit}"
test = f"ZCD Waveforms"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################


def routine(filename, vin):
    scope.run_single()
    soak(3)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
    input(">> Adjust cursor. Press ENTER to capture.")
    
    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

def choose_load_type(load_type):
    global path
    # load_type = int(input("\nSelect the following load:  \n1 - Incandescent \n2 - LED \n3 - Fan\n\n>> Enter choice and press ENTER to continue: "))
    if load_type == 1:
        load = "Incandescent"
    elif load_type == 2:
        EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SCALE(4, 5)
        EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_POSITION(4, 0)
        EQUIPMENT_FUNCTIONS().SCOPE().EDGE_TRIGGER(4, -2, 'NEG')
        load = "LED 17W"
    elif load_type == 3:
        EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SCALE(4, 0.5)
        EQUIPMENT_FUNCTIONS().SCOPE().EDGE_TRIGGER(4, 0.3, 'POS')
        load = "Fan 33W"
    else:
        load = None
    
    path = path_maker(waveforms_folder + f"\{load}")
    print(f"Load: {load}")
    return load


def main():
    scope_settings(SCOPE_CONFIG)
    load = choose_load_type(load_type)
    for vin in vin_list:

        # if vin == 120: scope.edge_trigger(trigger_channel=4, trigger_level=2.5, trigger_edge='POS')
        # if vin == 230: scope.edge_trigger(trigger_channel=4, trigger_level=2.5, trigger_edge='POS')

        filename = f"UNIT_{unit}_{load}_{vin}VAC_1st_Calibration_Pulse"
        routine(filename, vin)
        
        filename = f"UNIT_{unit}_{load}_{vin}VAC_2nd_ZC_Powerup"
        routine(filename, vin)
               
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

        soak(10)

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
