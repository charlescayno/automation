from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [200, 210, 230, 240]
soak_time = 5
soak_time_per_line = 5

# OUTPUT
excel_name = "test"
load_list = [(5,3), (9,2), (10,2.25)]

# PROJECT DETAILS
project = "140W Bull GaN"
test = f"Line Regulation"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    for vout, iout in load_list:
        df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD[:])
        input(">> Press ENTER to turn on AC")
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
        input(f"Set {vout}V/{iout}A")
        EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4, iout)
        
        
        i = 0
        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            if i == 0:
                soak(soak_time)
                i += 1
            else: soak(soak_time_per_line)
                
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, iout)
            export_to_excel(df, waveforms_folder, output_list, excel_name=f"{excel_name}_{vout}V_{iout}A", sheet_name=excel_name, anchor="A1")

        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)
        i = 0

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
