from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [100,277]

soak_time = 3
soak_time_per_line = 3
soak_time_per_load = 3

# OUTPUT
vout_nom_1 = 48
iout_nom_1 = 2.08

vout_nom_2 = 5
iout_nom_2 = 1

vout_nom_3 = 5
iout_nom_3 = 1

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-801"
results_folder = "Test Data"
test_name = f"Dimming"
unit_no = "1"
unit = f"{unit_no}"
excel_name = f'{unit_no}_{vout_nom_1}V'

waveforms_folder = f"C:/Users/{username}/Documents/{adf}/Work/{project_type}/{project_name}/{results_folder}/{unit}/{test_name}/{dt_string}/{vout_nom_1}V"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################
def main():

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS_with_dimming[:]
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    EQUIPMENT_FUNCTIONS().DC_SOURCE_TURN_ON(10)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for vin in vin_list:
        for load_1 in range(100, -1, -1):  # 100 → 0

            dim_voltage = 10*load_1/100

            if load_1 == 100: dim_voltage = 10
        
            print(f"Dimming = {load_1}%")
            EQUIPMENT_FUNCTIONS().DC_SOURCE_TURN_ON(dim_voltage)

            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(soak_time)
            

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, vout_nom_1, iout_nom_1, dim_voltage)

            export_to_excel(df, waveforms_folder, output_list, excel_name=f"{vout_nom_1}V {test_name}", sheet_name=f"{vout_nom_1}V {test_name}", anchor="A1")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

    EQUIPMENT_FUNCTIONS().DC_SOURCE_TURN_ON(10)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)