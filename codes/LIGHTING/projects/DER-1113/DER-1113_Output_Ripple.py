import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]

soak_time = 60
soak_time_per_line = 30
soak_time_per_load = 30

soak_time = 3
soak_time_per_line = 3
soak_time_per_load = 3

# OUTPUT
vout_nom_1 = 28
iout_nom_1 = 2.9

vout_nom_2 = 28
iout_nom_2 = 2.9

vout_nom_3 = 28
iout_nom_3 = 2.9
iout3_list = [i for i in range(100, -10, -10)]

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1113"
results_folder = "2. Data Result Spreadsheet"
unit_no = "2_MINUSONECAP_20mhz"
unit = f"Rev A_{unit_no}"
test_name = f"Ripple vs Load"

excel_name = f'{unit_no}_{vout_nom_1}V'

vds_channel = 1
channel_to_trigger = vds_channel
channel_trigger_delta = 0.01


scope_channel_list = [1]

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################

# HEADER_LIST_1CC_NORMAL = ['Vac (rms)', 'Freq (Hz)',
#                             'Vin (rms)', 'Iin (mA)', 'Pin (W)',
#                             'PF', '% THD',
#                             'Vo1 (V)', 'Io1 (mA)', 'Po1 (W)',
#                             '%V Reg1', 'Efficiency (%)']


def main():
    
    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CC_NORMAL[:]
    for channel in scope_channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

        for percent in iout3_list:
            EQUIPMENT_FUNCTIONS().SCOPE().RUN()
            EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()

            iout_3 = iout_nom_3 * percent / 100
            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_3)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(soak_time)
            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)
            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
            soak(2)
            filename = f"{test_name} {vin}VAC {vout_nom_3}V{iout_3}A Load={percent}%"
            EQUIPMENT_FUNCTIONS().SCOPE().STOP()
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
            
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_NORMAL_with_ripple(vin, vout_nom_3, iout_nom_3, scope_channel_list)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test_name}", anchor="A1")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)



if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)