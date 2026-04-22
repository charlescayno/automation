import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from misc_codes.scope_settings_der867_zcd_timings import *
from misc_codes.scope_setter import *

########################################## USER INPUT ##########################################
unit = 1
vin_list = [230]
load_type = 3

# PROJECT DETAILS
project = "DER-867"

excel_name = f"Unit {unit}"
test = f"3 - Set and Reset Time Calibration"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def choose_load_type(load_type):
    # load_type = int(input("\nSelect the following load:  \n1 - Incandescent \n2 - LED \n3 - Fan\n\n>> Enter choice and press ENTER to continue: "))
    if load_type == 1:
        load = "Incandescent"
        scope_settings(SCOPE_CONFIG)
    elif load_type == 2:
        load = "LED 17W"
        scope_settings(SCOPE_CONFIG_LED)
    elif load_type == 3:
        scope_settings(SCOPE_CONFIG_FAN)
        load = "Fan 33W"
    else:
        load = None
    print(f"Load: {load}")
    return load

def main():
    
    EQUIPMENT_FUNCTIONS().AC_CURRENT_PEAK(20)

    load = choose_load_type(load_type)

    
    choice = int(input("Press 1 for RelayON_Pulse, Press 2 for RelayOFF_Pulse: "))
    if choice == 1: scope.channel_settings(state='ON', channel=3, scale=1, position=-1, label="RelayON Pulse", color='LIGHT_BLUE', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)
    else: scope.channel_settings(state='ON', channel=3, scale=1, position=-1, label="RelayOFF Pulse", color='GREEN', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)


    for vin in vin_list:
        
        if choice == 1:
            j = "RelayON_pulse"
            scope.add_zoom(rel_pos=16.5, rel_scale=1)
        else:
            j = "RelayOFF_pulse"
            scope.add_zoom(rel_pos=33, rel_scale=1)

        scope.run_single()
        sleep(3)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        sleep(3)
        print("Turn switch on")
        sleep(3)
        print("Turn switch off")
        sleep(4)
        EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

        input("Capture waveform?")
        filename = f'Unit_{unit}, {load}, {j} - {vin}Vac, {ac.frequency}Hz'

        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
                
        if choice == 1: scope.add_zoom(rel_pos=53.15, rel_scale=1)
        else: scope.add_zoom(rel_pos=83.4, rel_scale=1)

        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT_LOOPER(filename, waveforms_folder)

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
