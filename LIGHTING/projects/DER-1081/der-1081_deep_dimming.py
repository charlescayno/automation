import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [230,265]

soak_time = 60
soak_time_per_line = 120
soak_time_per_load = 30

soak_time = 3
soak_time_per_line = 3
soak_time_per_load = 3

# OUTPUT
vout_nom_1 = 42
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0, 0.5]

vout_nom_3 = 42
iout_nom_3 = 1.2

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"

test_name = f"Deep dimming"
unit_no = "1"
unit = f"Rev C Samples_{unit_no}"
excel_name = f'{unit_no}_{vout_nom_1}V'



dim_freq = 10000
vds_channel = 2
channel_to_trigger = vds_channel
channel_trigger_delta = 1

scope_channel_list = [1,2,3]

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{unit}/{test_name}/{dt_string}/{vout_nom_1}V"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################
def main():
    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/DER-1081/DEEP DIMMING.dfl'")

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS_with_dimming[:]
    for channel in scope_channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for iout2 in iout2_list:
        for vin in vin_list:
            for load_1 in np.arange(4, -0.05, -0.05):
                if load_1 == 100:
                    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
                    print(load_1)
                if load_1 <= 0.1:
                    EQUIPMENT_FUNCTIONS().SIG_GEN(0.02, dim_freq)
                    load_1 = 0.02
                
                print(load_1)

                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)
                EQUIPMENT_FUNCTIONS().SCOPE().RUN()
                EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()
                EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                soak(soak_time)

                filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
                EQUIPMENT_FUNCTIONS().SCOPE().STOP()

                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS_with_dimming(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, dim_freq, load_1, scope_channel_list)

                export_to_excel(df, waveforms_folder, output_list, excel_name=f"{vout_nom_1}V {test_name}", sheet_name=f"{vout_nom_1}V {test_name}", anchor="A1")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)