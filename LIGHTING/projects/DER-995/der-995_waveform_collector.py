import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 200, 230, 240, 265]
vin_list = [180,230,265]


# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

# PROJECT DETAILS
project = "DER-995"
test = f"Stress"
component = f"D2"
# unit = input(">> Enter unit number: ")
unit = "TRF3"
excel_name = f'{project}_{test}_{unit}'

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)


wavecapture_enabled = True
channel_to_trigger = 1
channel_trigger_delta = 1
########################################## USER INPUT ##########################################


def main():

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC[:])

    EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=3, current=0.1)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        sleep(5)
        input()
        
        filename = f"{component}_{vin}Vac_LED_{vout_nom_1}V_{iout_nom_1}A_CV2_{vout_nom_2}V_{iout_nom_2}A_CV1_{vout_nom_3}V_{iout_nom_3}A"
        if wavecapture_enabled:
            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=channel_to_trigger, trigger_delta=channel_trigger_delta)
            # prompt("Capture_waveform")
            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
            soak(2)
            path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)