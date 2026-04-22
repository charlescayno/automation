from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
# vin_list = [195, 200, 230, 240, 265]
vin_list = [195, 230, 265]

soak_time = 60
soak_time_per_line = 60
soak_time_per_load = 30

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 42
vout1_list = [42,12]
# vout_nom_1 = 12
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0.5,0]

vout_nom_3 = 12
iout_nom_3 = 1.2


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = f"Input Current Waveform"
unit = f"{test_name}_{vout_nom_1}V"
excel_name = f'{unit}_{time_string}'


vds_channel = 1
channel_to_trigger = vds_channel
channel_trigger_delta = 0.05

scope_channel_list = [1]

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():

    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/der-1081-input-current.dfl'")
    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS[:]
    for channel in scope_channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)



    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for vout1 in vout1_list:

        input(f">> Change LED voltage to: {vout1}V")

        for iout2 in iout2_list:
        
            for vin in vin_list:    
                EQUIPMENT_FUNCTIONS().SCOPE().RUN()
                EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()

                EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                # input()
                soak(soak_time)
                EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)
                EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
                soak(2)
                # input(">> Capture waveform and continue? ")
                filename = f"{test_name} {vin}VAC {vout1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
                EQUIPMENT_FUNCTIONS().SCOPE().STOP()
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS(vin, vout1, vout_nom_2, iout_nom_1, iout_nom_2, scope_channel_list)
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test_name}", anchor="A1")
                # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
                
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
            

        

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)