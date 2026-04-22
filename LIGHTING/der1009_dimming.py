from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 200, 230, 265]

soak_time = 30
delay_per_line = 30
delay_per_load_step = 30

# OUTPUT
vout = 36
iout = 0.8
dim_list = [4, 3, 2, 1, 0]

# PROJECT DETAILS
project = "DER-1009"
excel_name = "Dimming"
test = f"Line Regulation"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_DIM)

    for dim in dim_list:

        input(f"Set voltage to {dim} volts")

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
        soak(soak_time)

        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(delay_per_line)

            
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_DIMMING(vin, vout, iout, dim)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
