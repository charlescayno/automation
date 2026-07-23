import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [195,230,265,277]
# vin_list = [195, 200, 210, 220, 230, 240, 265, 277]

soak_time = 60
soak_time_per_line = 60
soak_time_per_load = 30

# OUTPUT
vout_nom_1 = 54
# vout_nom_1 = 12
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0.5, 0.4, 0.3, 0.2, 0.1, 0]
iout2_list = [0.5]

vout_nom_3 = 12
iout_nom_3 = 1.2


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = f"CSA Steady-state (D1-470pF)"
unit = f"2"
excel_name = f'{unit}_{time_string}'

channel_to_trigger = 2
channel_trigger_delta = 1

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():
   
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRFETVDS_Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRFETVDS_Steadystate_wfsw.dfl'")
    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for vin in vin_list:

        for iout2 in iout2_list:
            EQUIPMENT_FUNCTIONS().SCOPE().RUN()
            EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()

            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(4)
            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)
            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
            soak(2)
            # input(">> Capture waveform and continue? ")
            filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
            EQUIPMENT_FUNCTIONS().SCOPE().STOP()
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
            

        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)