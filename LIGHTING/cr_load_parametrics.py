from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180,200,210,220,230,264]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK
# OUTPUT
vout = 59
iout = 1.98
percent_list = [100] # percent_list = range(100, -1, -1) # 100% to 0% loading
cr_list = [((vout/iout)*100/percent if percent != 0 else 0) for percent in percent_list]
# PROJECT DETAILS
# project = input(">> Project: ")
project = "DER-580 CVCC Curve Modification"
excel_name = input(">> Excel Name: ")
test = f"Parametrics - CR Load"
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################


def main():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CR_LOAD)
    
    for cr in cr_list:
        EQUIPMENT_FUNCTIONS().ELOAD_CR_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cr/0.5, 0)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(180)
        soak(5)

    
    for cr in cr_list:

        # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
        EQUIPMENT_FUNCTIONS().ELOAD_CR_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cr, 0)

        for vin in vin_list:

            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(soak_time_per_line)
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CR_LOAD(vin, vout, cr)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

        
if __name__ == "__main__":
    estimated_time =  len(vin_list)*soak_time_per_line
    GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    headers(test)
    main()
    footers(waveform_counter)
