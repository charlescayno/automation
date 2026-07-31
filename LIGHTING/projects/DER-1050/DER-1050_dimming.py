import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]
vin_list = [230]

soak_time = 5
soak_time_per_line = 5
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
project = "DER-1050"
test = f"Dimminsg"
unit = "Rev B"
excel_name = f'{project}_{unit}'

from datetime import datetime
now = datetime.now()
print("now =", now)
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
print("date and time =", dt_string)

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{dt_string}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path


dim_freq = 10000
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

    load_list_1a = np.arange(0, 4, 1)
    print(load_list_1a)
    load_list_1b = np.arange(4, 100, 1)
    test_total_counter = (len(load_list_1a) + len(load_list_1b)) * len(vin_list)
    test_total_time = EQUIPMENT_FUNCTIONS().two_sig_fig(test_total_counter*soak_time_per_load/60)
    print(f"Total test items: {test_total_counter}. Approx. test time: {test_total_time} mins.")
    counter = 0


    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_dimming[:])

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)
    EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
    
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)
    input("Change code this is an intervention just to use dimming hahaha.J ")

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        for load_1 in load_list_1a:
            counter += 1
            test_time = EQUIPMENT_FUNCTIONS().two_sig_fig((test_total_counter-counter)*soak_time_per_load/60)
            print(f">> Test on-going ({counter}/{test_total_counter})... Approx. time left: {test_time} mins.\n")

            if load_1 >= 99:
                ENABLE_DIMMING()
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)

            soak(soak_time_per_load)
        
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_dimming(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, duty=load_1)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
        
        for load_1 in load_list_1b:
            counter += 1
            test_time = EQUIPMENT_FUNCTIONS().two_sig_fig((test_total_counter-counter)*soak_time_per_load/60)
            print(f">> Test on-going ({counter}/{test_total_counter})... Approx. time left: {test_time} mins.\n")

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