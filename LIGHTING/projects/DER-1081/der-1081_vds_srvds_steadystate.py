import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [195, 200, 230, 240, 265, 277]

soak_time = 60
soak_time_per_line = 60
soak_time_per_load = 30

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 48
# vout_nom_1 = 12
iout_nom_1 = 1.3

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0.5]

vout_nom_3 = 12
iout_nom_3 = 1.2


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = f"Steadystate Pri VDS"
# test_name = f"Steadystate SRFET VDS"
unit = f"2-final (1.2A)"
excel_name = f'{unit}_{time_string}'


vds_channel = 1
channel_to_trigger = vds_channel
channel_trigger_delta = 1

scope_channel_list = [1]

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():
    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/DER-1081 Primary Vds Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/DER-1081 SRFET Vds Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRDiode_Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRDiode_Steadystate_with_VC22.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRFETVDS_Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRFETVDS_Steadystate_wfsw.dfl'")

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS[:]
    for channel in scope_channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)



    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for vin in vin_list:

        for iout2 in iout2_list:
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
            filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
            EQUIPMENT_FUNCTIONS().SCOPE().STOP()
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, scope_channel_list)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test_name}", anchor="A1")
            # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
            
        # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
            

        

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)