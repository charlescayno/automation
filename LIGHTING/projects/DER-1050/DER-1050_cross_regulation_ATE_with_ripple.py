import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180,230,265]
vin_list = [230]


soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

# LOAD INCREMENT STEPS IN PERCENT
load_increment_1 = 100           # %
load_increment_2 = 10           # %
load_increment_3 = 10           # %

channel_list = [1,2,3,4]
print(">> Set current probe at CH3 - IOUT")
print(">> Set dimming source")
input(">> Press ENTER to continue... ")

# PROJECT DETAILS
project = "DER-1050"
test = f"Cross Reg, SVF Disabled"
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
    # pass

def LOAD_LIST(load_increment):
    temp_list = list(np.arange(0, 100+load_increment, load_increment))
    temp_list.sort(reverse=True)
    load_list = list(np.divide(temp_list, 100))
    print(load_list)
    return load_list

def main():

    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/der995-ripple.dfl'")

    load_list_1 = [100,90,80,70,60,50,40,30,20,10,0]
    # load_list_1 = [30,10,0]
    load_list_2 = LOAD_LIST(load_increment_2)
    load_list_3 = LOAD_LIST(load_increment_3)
    test_total_counter = len(load_list_1) * len(load_list_2) * len(load_list_3) * len(vin_list)
    test_total_time = EQUIPMENT_FUNCTIONS().two_sig_fig(test_total_counter*soak_time_per_load/60)
    print(f"Total test items: {test_total_counter}. Approx. test time: {test_total_time} mins.")
    counter = 0

    
    header_list = GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_cross_reg[:]
    for channel in channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    ENABLE_DIMMING()
    # input(f">> Set duty to 99%")

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    
    sleep(2)


    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)
        
        for load_1 in load_list_1:
            if load_1 >= 99:
                ENABLE_DIMMING()
                # input(f">> Set duty to 99%")
            elif load_1 == 0:
                EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, dim_freq)
                # input(f">> Set duty to 0%")
            else:
                EQUIPMENT_FUNCTIONS().SIG_GEN(load_1, dim_freq)
                # input(f">> Set duty to {load_1}%")
            
            for load_3 in load_list_3:
                for load_2 in load_list_2:
                    
                    counter += 1
                    test_time = EQUIPMENT_FUNCTIONS().two_sig_fig((test_total_counter-counter)*soak_time_per_load/60)
                    print(f">> Test on-going ({counter}/{test_total_counter})... Approx. time left: {test_time} mins.\n")
                          
                    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
                    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2*load_2, iout_nom_3*load_3)

                    output_power_1 = EQUIPMENT_FUNCTIONS().two_sig_fig(vout_nom_1*load_1*iout_nom_1/100)
                    output_power_2 = EQUIPMENT_FUNCTIONS().two_sig_fig(vout_nom_2*iout_nom_2*load_2)
                    output_power_3 = vout_nom_3*load_3*iout_nom_3
                    total_output_power = EQUIPMENT_FUNCTIONS().two_sig_fig(output_power_1 + output_power_2 + output_power_3)
                    soak(soak_time_per_load)

                    CV2_load = EQUIPMENT_FUNCTIONS().two_sig_fig(load_2*100)
                    CV1_load = EQUIPMENT_FUNCTIONS().two_sig_fig(load_3*100)
                    filename = f"{vin}VAC_Po_{total_output_power}W__{vout_nom_1}V_{load_1}Load__CV2_{vout_nom_2}V_{CV2_load}%Load__CV1_{vout_nom_3}V_{CV1_load}%Load"
                    # print(filename)                  

                    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_cross_reg_ripple(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, load_1, load_2*100, load_3*100, channel_list)
                    export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")

                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}/{unit}")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
    # EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)