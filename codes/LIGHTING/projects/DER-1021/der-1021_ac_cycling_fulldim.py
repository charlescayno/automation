import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120,230]
# vin_list = [120]

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1

# OUTPUT
led_load_list = [42,36]



vout_nom_1 = 36
iout_nom_1 = 3.57

vout_nom_2 = 6
iout_nom_2 = 0

vout_nom_3 = 12
iout_nom_3 = 0


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1021"
results_folder = "Marketing Samples"
test_name = f"AC Cycling Dim=11V"
unit = f"ph unit 2"
excel_name = f'{unit}_{time_string}'


waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
print(path)
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():

    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/der1021_accyclingdimshort.dfl'")

    input(f">> OPEN DIM pin")

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)


    for led_load in led_load_list:

        input(f">> Change LED to {led_load}V")

        for vin in vin_list:
            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            sleep(2)
            sleep(4)
            EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
            sleep(1)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            sleep(1)
            EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
            sleep(1)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            sleep(1)

            sleep(9)

            EQUIPMENT_FUNCTIONS().SCOPE().STOP()


            iout = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()

            input(">> Adjust cursor")

            filename = f"{vin}VAC, {led_load}V, AC Cyling Dim=11V"
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)

        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)
    
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)
            

        

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)