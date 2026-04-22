## This is a starup operation code, set Vds at Ch2

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 5.8

vout_nom_3 = 5
iout_nom_3 = 0.5


# PROJECT DETAILS
project = "DER-1050"
test = f"Steady-state"
unit = "Rev B"
component = f"Disabled LED PLIM Delay After Standby (DC DIM)"

channel_to_trigger = 2
channel_trigger_delta = 2
capture_manual = False
wavecapture_enabled = True

excel_name = f'{component}_startup'

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{component}/"
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
    # df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_with_VDS_MAX[:])
    # EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=3, current=0.1)
    
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, 10000)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
        sleep(5)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        filename = f"{vin}Vac_{vout_nom_1}V_{iout_nom_1}A__{vout_nom_2}V_{iout_nom_2}A__{vout_nom_3}V_{iout_nom_3}A"
        if wavecapture_enabled:
            soak(6)
            # output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_with_VDS_MAX(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, channel_to_trigger)
            # export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{component}", anchor="A1")
            if capture_manual: input(">> Capture waveform? ")
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

def main_steadystate():
    # EQUIPMENT_FUNCTIONS().SIG_GEN(99, 10000)
    EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=3.3, current=0.1)
    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        sleep(2)

        # EQUIPMENT_FUNCTIONS().SIG_GEN(0.016, 10000)
        EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=0, current=0.1)
        sleep(3)

        EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
        sleep(3)

        # EQUIPMENT_FUNCTIONS().SIG_GEN(99, 10000)
        EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=3.3, current=0.1)
        sleep(3)
        filename = f"{vin}Vac_{vout_nom_1}V_{iout_nom_1}A__{vout_nom_2}V_{iout_nom_2}A__{vout_nom_3}V_{iout_nom_3}A"
        if wavecapture_enabled:
            if capture_manual: input(">> Capture waveform? ")
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    # adjust_scope()
    main_steadystate()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)