import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [195, 200, 230, 240, 265]
soak_time = 60

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0, 0.5]

vout_nom_3 = 12
iout_nom_3 = 1.2

# PROJECT DETAILS
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

project_type = "DER"
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = "IDS VDS Steady State"
unit = f"{test_name}_{vout_nom_1}V"
excel_name = f"{unit}_{time_string}"

channel_to_trigger = 1
channel_trigger_delta = 0.01
scope_channel_list = [1]

waveforms_folder = path_maker(f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/")
########################################## USER INPUT ##########################################


def main():

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    sc.POSITION_SCALE(time_position=20, time_scale=5E-6)
    sc.CHANNEL_SETTINGS(state='ON', channel=1, scale=1, position=1, label="IDS", color='LIGHT_BLUE', rel_x_position=30, bandwidth=500, coupling='DCLimit', offset=0)
    sc.CHANNEL_SETTINGS(state='ON', channel=2, scale=200, position=-4, label="VDS", color='YELLOW', rel_x_position=40, bandwidth=500, coupling='DCLimit', offset=0)

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS[:]
    for channel in scope_channel_list:
        header_list = ef.APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = gf.CREATE_DF_WITH_HEADER(header_list)

    ef.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for iout2 in iout2_list:
        for vin in vin_list:

            sc.RUN()
            ef.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
            ef.AC_TURN_ON(vin)
            soak(soak_time)
            ef.FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)
            sc.RUN_SINGLE()
            soak(2)
            filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
            sc.STOP()
            sc.SCOPE_SCREENSHOT(filename, waveforms_folder)

            output_list = ef.COLLECT_DATA_1CV_1CC_PARAMETRICS(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout2, scope_channel_list)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=test_name, anchor="A1")

    gf.PRINT_FINAL_DATA_DF(df)
    ef.DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
