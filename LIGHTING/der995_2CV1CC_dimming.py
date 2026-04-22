from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 200, 230, 265]
vin_list = [230]

soak_time = 3
soak_time_per_line = 3
soak_time_per_load = 5

# soak_time = 3
# soak_time_per_line = 3
# soak_time_per_load = 3

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

load_increment_1 = 10

# PROJECT DETAILS
project = "DER-995"
test = f"Dimming"
# unit = input(">> Enter unit number: ")

unit = "TRF5 with shield iteration21 550uH"
unit = "TRF5 1x560uF 2x1200uF fine dimming"

excel_name = f'{project}_{test}_{unit}'
excel_name = f'{project}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)


dim_freq = 1000
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

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_dimming[:])

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)
    EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        load_list_1 = LOAD_LIST(load_increment_1)

        for load_1 in np.arange(0, 4.01, 0.001):
            if load_1 >= 99:
                ENABLE_DIMMING()
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)

            soak(soak_time_per_load)
        
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_dimming(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, duty=load_1)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
        for load_1 in np.arange(4, 100, 1):
            if load_1 >= 99:
                ENABLE_DIMMING()
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)

            soak(soak_time_per_load)
        
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_dimming(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, duty=load_1)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
                
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)