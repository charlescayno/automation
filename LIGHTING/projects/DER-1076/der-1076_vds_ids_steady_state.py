import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
## This is a starup operation code, set Vds at Ch2

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import sys
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 115, 230, 265]
vin_list = [265]
vin_list = [115,230]
# vin_list = [90,115,230,265]

# OUTPUT
vout_nom_1 = 24
iout_nom_1 = 1.7
percent_list = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

vout_nom_2 = 0
iout_nom_2 = 0

vout_nom_3 = 0
iout_nom_3 = 0


# PROJECT DETAILS
project = "DER-1076"
test = f"Steady-state"
unit = "Rev A"
component = f"Vout Ripple"
rework = "default"
# rework = sys.argv[1]
excel_name = rework

channel_to_trigger = 1
channel_trigger_delta = 0.001
capture_manual = False
wavecapture_enabled = True

# excel_name = f'{component}_startup'

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/2 - Test Data/{test}/{unit}/{component}/"
path = path_maker(f'{waveforms_folder}')


pout_nom_1 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_1*iout_nom_1, 0)
pout_nom_2 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_2*iout_nom_2, 0)
pout_nom_3 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_3*iout_nom_3, 0)
########################################## USER INPUT ##########################################

def adjust_scope():
    EQUIPMENT_FUNCTIONS().SCOPE().TIME_SCALE(100E-3)
    EQUIPMENT_FUNCTIONS().SCOPE().LABEL(channel_to_trigger, component, 25)
    EQUIPMENT_FUNCTIONS().SCOPE().EDGE_TRIGGER(channel_to_trigger, 50, 'POS')
    EQUIPMENT_FUNCTIONS().SCOPE().TIME_POSITION(10)

def main_startup():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_with_VDS_MAX[:])
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
        sleep(5)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        filename = f"{vin}Vac_{vout_nom_1}V_{iout_nom_1}A"
        if wavecapture_enabled:
            soak(6)
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_with_VDS_MAX(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, channel_to_trigger)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{component}", anchor="A1")
            if capture_manual: input(">> Capture waveform? ")
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

def main_steadystate():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_PDEL[:])

    for vin in vin_list:
        cc_list = [((iout_nom_1)*percent/100 if percent != 0 else 0) for percent in percent_list]

        for cc in cc_list:

            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(cc, cc, cc)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            sleep(2)

            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)

            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()

            sleep(3)
            filename = f"{vin}Vac_{vout_nom_1}V_{cc}A_{rework}"

            if wavecapture_enabled:
                if capture_manual: input(">> Capture waveform? ")
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL(vin, vout_nom_1, cc, 100)
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{component}", anchor="A1")
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    # adjust_scope()
    main_steadystate()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)