import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]
# vin_list = [230]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 10

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

# LOAD INCREMENT STEPS IN PERCENT
load_increment_1 = 100           # %
load_increment_2 = 25           # %
load_increment_3 = 25           # %

# PROJECT DETAILS
project = "DER-995"
test = f"Cross Regulation"
# unit = input(">> Enter unit number: ")
unit = "TRF4"
excel_name = f'{project}_{test}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)

dim_freq = 1000
########################################## USER INPUT ##########################################

def ENABLE_DIMMING():
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, 1000)

def LOAD_LIST(load_increment):
    temp_list = list(np.arange(0, 100+load_increment, load_increment))
    temp_list.sort(reverse=True)
    load_list = list(np.divide(temp_list, 100))
    print(load_list)
    return load_list


def main():

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_cross_reg[:])

    ENABLE_DIMMING()
    input()

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)
        
        load_list_1 = [100,50,10,0]
        load_list_2 = LOAD_LIST(load_increment_2)
        load_list_3 = LOAD_LIST(load_increment_3)

        for load_1 in load_list_1:
            if load_1 >= 99:
                ENABLE_DIMMING()
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)
            for load_2 in load_list_2:
                for load_3 in load_list_3:
                    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2*load_2, iout_nom_3*load_3)
                    print(f"Vin = {vin} VAC, Dimming = {load_1} %, CV2: {load_2*100} %, CV3: {load_3*100} %")
        
                    soak(soak_time_per_load)

                    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_cross_reg(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, load_1, load_2*100, load_3*100)
                    export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
                
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)