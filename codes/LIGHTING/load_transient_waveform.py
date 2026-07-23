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
# load_list_1 = [(5,3)]
load_list_1 = [(9,3),(12,3),(15,3),(20,3.25)]
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
test = f"Load Transient"
unit = 6
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/04 - Waveforms/01 - {test}/Unit {unit}"

# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################



def main():
    input("Press ENTER to turn on AC")

    for vout1, iout1 in load_list_1:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        print(f"Set {port}: {vout1}V")
        input("Set PD ports")

        for low_percent, high_percent in load_transient_percent_list:

            for vin in vin_list:
                
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                low = low_percent*iout1/100
                high = high_percent*iout1/100
                mid = (low+high)/2
                ton = (1/load_transient_frequency)/2
                toff = ton
                EQUIPMENT_FUNCTIONS().ELOAD_LOAD_TRANSIENT(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, low, high, ton, toff)
                EQUIPMENT_FUNCTIONS().SCOPE().EDGE_TRIGGER(trigger_channel, mid, 'POS')
                scope.channel_offset(1, vout1-1)
                
                scope.run()
                scope.trigger_mode(mode='NORM')
                soak(3)
                scope.run_single()
                soak(5)

                filename = f"{test}_{vin}Vac_{vout1}V_{iout1}A_{low_percent}-{high_percent}%"

                if wavecapture_enabled:
                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
