from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]

soak_time = 60
soak_time_per_line = 30
soak_time_per_load = 30

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 28
iout_nom_1 = 1.9

vout_nom_2 = 28
iout_nom_2 = 1.9

vout_nom_3 = 28
iout_nom_3 = 1.9


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1113"
results_folder = "2. Data Result Spreadsheet"
unit_no = "2"
unit = f"Rev A_{unit_no}"
test_name = f"Efficiency vs Input Voltage"

excel_name = f'{unit_no}_{vout_nom_1}V'

channel_to_trigger = 1
channel_trigger_delta = 5

# scope_channel_list = [1,2,3]

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
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        sleep(3)
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

        sleep(3)

        soak(soak_time)
        soak(2)
        

        output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_NORMAL(vin, vout_nom_1, iout_nom_1)
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