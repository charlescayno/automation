from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [230]

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 42
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0.5, 0]

vout_nom_3 = 12
iout_nom_3 = 1.2

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = f"AC Cycling Debugging"
component = "Rev B_Marketing_Samples"
unit = f"Rev B_new unit"
excel_name = f'{unit}_{time_string}'

dim_freq = 10000
vds_channel = 2
channel_to_trigger = vds_channel
channel_trigger_delta = 1

scope_channel_list = [2,3,4]
scope_channel_list = [1]

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{unit}/{test_name}/{dt_string}/{vout_nom_1}V"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################
def main():

    # EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
    # input()

    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(1, 2, 0.5)

    # for vin in vin_list:
    #     for iout2 in iout2_list:
    #         for load_1 in np.arange(4, -0.05, -0.05):
    #             if load_1 == 100:
    #                 EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
    #                 print(load_1)
    #             if load_1 <= 0.1:
    #                 EQUIPMENT_FUNCTIONS().SIG_GEN(0.02, dim_freq)
    #                 load_1 = 0.02
                
    #             print(load_1)

    #             EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)
    #             EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    #             EQUIPMENT_FUNCTIONS().SCOPE().MODE_AUTO()
    #             EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
    #             EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
    #             soak(soak_time)
    #             # EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)
    #             # EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
    #             # soak(2)
    #             # input(">> Capture waveform and continue? ")
    #             filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
    #             EQUIPMENT_FUNCTIONS().SCOPE().STOP()
    #             # EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

    #             output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CV_1CC_PARAMETRICS_with_dimming(vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, dim_freq, load_1, scope_channel_list)

    #             export_to_excel(df, waveforms_folder, output_list, excel_name=f"{vout_nom_1}V {test_name}", sheet_name=f"{vout_nom_1}V {test_name}", anchor="A1")

    # GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

    # EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
            

        

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)