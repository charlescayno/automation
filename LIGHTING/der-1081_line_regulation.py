from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [195,200,220,230,240,265,277]
vin_list = [230]

soak_time = 60
soak_time_per_line = 30
soak_time_per_load = 30

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 30

# OUTPUT
vout_nom_1 = 48
iout_nom_1 = 1.2

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
test_name = f"Dimming"
unit = f"1"
excel_name = f'{unit}_{time_string}'
rework = "_"

scope_channel_list = [1]

dim_freq = 10000


vds_channel = 1
waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def ENABLE_DIMMING():
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, 1000)

def LOAD_LIST(load_increment):
    temp_list = list(np.arange(0, 100+load_increment, load_increment))
    temp_list.sort(reverse=False)
    load_list = temp_list
    print(load_list)
    return load_list


def main():

    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRFETVDS_Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/VDS_SRDiode_Steadystate.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/DER-1081 Primary Vds Steadystate.dfl'")

    load_list_1a = np.arange(0, 4, 1)
    print(load_list_1a)
    load_list_1b = np.arange(4, 101, 1)
    print(load_list_1b)

    EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
    
    # EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
    # input("Change code this is an intervention just to use dimming hahaha.J ")
    
    
    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS_with_dimming[:]
    for channel in scope_channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:


        for load_1 in load_list_1a:
            if load_1 >= 99:
                ENABLE_DIMMING()
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)
            
            for iout2 in iout2_list:
                EQUIPMENT_FUNCTIONS().SCOPE().RUN()
                EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                soak(soak_time_per_line)
                filename = f"{rework} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
                EQUIPMENT_FUNCTIONS().SCOPE().STOP()
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
                
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS_with_dimming(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, dim_freq, load_1, scope_channel_list)
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test_name}", anchor="A1")


        for load_2 in load_list_1b:
            if load_2 >= 99:
                ENABLE_DIMMING()
            elif load_2 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_2, dim_freq)
            
            for iout2 in iout2_list:
                EQUIPMENT_FUNCTIONS().SCOPE().RUN()
                EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                soak(soak_time_per_line)
                filename = f"{rework} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
                EQUIPMENT_FUNCTIONS().SCOPE().STOP()
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)
                
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS_with_dimming(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, dim_freq, load_2, scope_channel_list)
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