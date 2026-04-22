import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 200, 230, 240, 265]
vin_list = [230]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30

soak_time = 10
soak_time_per_line = 10
soak_time_per_load = 10

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

# PROJECT DETAILS
project = "DER-995"
test = f"Parametrics"
unit = "output power at 5V_1"
# unit = "test"
excel_name = f'{project}_{test}_{unit}'
excel_name = f'{project}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)

dim_freq = 1000
########################################## USER INPUT ##########################################
def main():

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC[:])

    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, 0)
    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        load_list = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5]

        

        for load in np.arange(0, 0.51, 0.01):
            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, load)
            soak(soak_time_per_load)

        
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, load)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
                
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)