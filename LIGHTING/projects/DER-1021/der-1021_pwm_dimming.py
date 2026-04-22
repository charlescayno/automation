import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120,230]
# vin_list = [120]

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 3.57

vout_nom_2 = 6
iout_nom_2 = 0

vout_nom_3 = 12
iout_nom_3 = 0


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1021"
results_folder = "Marketing Samples"
test_name = f"PWM Dimming"
dim_freq = 300
unit = f"ph unit 2-36V_300z"
excel_name = f'{unit}_{time_string}'


waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CC_with_dimming[:]

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
            
    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().SIG_GEN_10VPP(0.02, dim_freq)
        soak(5)

        # input("Start dimming")

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        for load_1 in np.arange(0, 101, 1):

            EQUIPMENT_FUNCTIONS().SIG_GEN_10VPP(load_1, dim_freq)

            if load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN_10VPP(0.02, dim_freq)
                soak(60)

            cc = iout_nom_1*load_1/100
            print(cc)
            soak(soak_time_per_load)
            
            

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_DIMMING(vin, vout_nom_1, cc, load_1)
            
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test_name}", anchor="A1")

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