from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [195, 200, 230, 240, 265]

soak_time = 5
soak_time_per_line = 10
soak_time_per_load = 5
integration_time_seconds = 120

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()


project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = f"No Load"
component = "Rev B_2x44uF_100R_2x150VSR_svfratio0pt7"
unit = f"Rev B"
excel_name = f'{unit}_{time_string}'
waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/{component}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path

########################################## USER INPUT ##########################################

def main():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_NO_LOAD[:])
    input(">> Remove loading, retain output voltage sense, and change switch to NL configuration")
    input("Press ENTER to turn on AC")

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    # soak(5)
    # EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
    
    i = 0
    for vin in vin_list:
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

        if i == 0:
            print(f"soak input for {soak_time}s")
            soak(soak_time)
            i += 1
                
        else:
            print(f"soak input for {soak_time_per_line}s")
            soak(soak_time_per_line)
            

        pms.integrate(integration_time_seconds)
        soak(integration_time_seconds+5)

        output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_NO_LOAD(vin)
        file_name = f"{excel_name}"
        export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

        i = 0

        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

        

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
