from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

########################################## USER INPUT ##########################################
led_list = convert_argv_to_int_list(">> led_list (48,36,24): ")
iout = float(input(">> Iout (A): "))

vin_list = GENERAL_CONSTANTS.DEFAULT_WIDE_RANGE_VIN_LIST
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK

project = input(">> Project: ")
test = f"Parametrics - LED"
excel_name = input(">> Excel Name: ")
########################################## USER INPUT ##########################################
waveforms_folder = GENERAL_FUNCTIONS.CREATE_PATH(project, test)

def main():
    df = GENERAL_FUNCTIONS.CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD)
    
    EQUIPMENT_FUNCTIONS.DISCHARGE_OUTPUT(1)

    for led in led_list:

        EQUIPMENT_FUNCTIONS.SET_LED(led)

        for vin in vin_list:

            EQUIPMENT_FUNCTIONS.AC_TURN_ON(vin)
            soak(soak_time_per_line)
            output_list = EQUIPMENT_FUNCTIONS.COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD(vin, led, iout)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

        GENERAL_FUNCTIONS.PRINT_FINAL_DATA_DF(df)
        EQUIPMENT_FUNCTIONS.DISCHARGE_OUTPUT(2)

        
if __name__ == "__main__":
    estimated_time =  len(vin_list)*soak_time_per_line
    GENERAL_FUNCTIONS.ESTIMATED_TEST_TIME(estimated_time)

    headers(test)
    main()
    footers(waveform_counter)
