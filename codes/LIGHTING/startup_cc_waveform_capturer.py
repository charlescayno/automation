"""
- manual setup of scope: CH1 vout (0.5V), CH2 iout (2A)
- auto offset of vout channel using x100 probe

"""

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,115,132]

soak_time = 7
soak_time_per_line = 7
soak_time_per_load = 7

# OUTPUT
load_list_1 = [(5,3)]
# load_list_1 = [(9,3),(12,3),(15,3),(20,3.25)]
# load_list_1 = [(12,3)]
# load_list_1 = [(15,3)]
# load_list_1 = [(20,3.25)]

load_transient_percent_list = [(10,100)]
load_transient_frequency = 25
port = "C1"
trigger_channel = 2

# PROJECT DETAILS
wavecapture_enabled = True
project = "DER-1024 Rev A"
test = f"Output Startup"
unit = 6
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/04 - Waveforms/01 - {test}/Unit {unit}"

# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################



def main():

    
    

    for vout1, iout1 in load_list_1:

        for vin in vin_list:

            EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(1, 3)

            scope.run_single()

            sleep(1)

            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

            filename = f"{test}_{vin}Vac_{vout1}V_{iout1}A"

            if wavecapture_enabled:
                sleep(3)
                path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)


            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

                

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
