from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from powi.equipment import prompt
import sys

########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 100, 110, 115, 120, 132]
vin_list = [90, 100, 115, 132]
# vin_list = [90, 115]

soak_time_initial = 30
soak_time_per_line = 30
soak_time_per_load = 30

soak_time_initial = 1
soak_time_per_line = 1
soak_time_per_load = 1


# OUTPUT

load_list_1 = [(20,3.25)]
load_list_2 = [(20,1)]

port1 = "C1"
port2 = "C2"

percent_list = [100, 75, 50, 25, 10, 0]
percent_list = [100]


# PROJECT DETAILS
project = "DER-1024 Rev B"
unit = input(">> Enter unit number: ")
test = f"Line Regulation"


excel_name = f"{unit}"
# datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/No Potting/{test}/{unit}"
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/XX - Marketing Samples/{test}/"

# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################

def main():
    # prompt("Press ENTER to turn on AC")

    initial_soak = True
    initial_vin = vin_list[0]

    print()
    print(f"Initial Soak: {soak_time_initial}s")
    print(f"Soak per Line: {soak_time_per_line}s")
    print(f"Soak per Load: {soak_time_per_load}s")
    print()


    for vout1, iout1 in load_list_1:
        for vout2, iout2 in load_list_2:

            df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_2[:])
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(initial_vin)

            
            print(f"Set {port1}: {vout1}V/{iout1}A")
            print(f"Set {port2}: {vout2}V/{iout2}A")
            # prompt("Set PD ports")
            sleep(3)
            
            c1 = EQUIPMENT_FUNCTIONS()._sigfig(vout1*iout1, 0)
            c2 = EQUIPMENT_FUNCTIONS()._sigfig(vout2*iout2, 0)
            # excel_name = f"{c1+c2}W"
            
            print(excel_name)
            
            
            for vin in vin_list:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                
                cc_list_1 = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
                cc_list_2 = [((iout2)*percent/100 if percent != 0 else 0) for percent in percent_list]

                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list_1[0])
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc_list_2[0])

                if initial_soak:
                    
                    soak(soak_time_initial)
                    initial_soak = False
                    
                else:

                    soak(soak_time_per_line)
                
                iout_list = [list(x) for x in zip(cc_list_1, cc_list_2)]

                for io1, io2 in iout_list:
                    soak(soak_time_per_load)

                    percent = EQUIPMENT_FUNCTIONS()._sigfig(io1*100/iout1, 0)
                    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_2(vin, vout1, vout2, io1, io2, percent)

                    export_to_excel(df, waveforms_folder, output_list, excel_name=f"{unit}_C1 {vout1}V{iout1}A_C2 {vout2}V{iout2}A", sheet_name=excel_name, anchor="A1")

                if len(percent_list) != 1:
                    output_list = EQUIPMENT_FUNCTIONS().BLANK_SPACE(df)
                    export_to_excel(df, waveforms_folder, output_list, excel_name=f"{unit}_C1 {vout1}V{iout1}A_C2 {vout2}V{iout2}A", sheet_name=excel_name, anchor="A1")

            initial_soak = True
            
            EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
            EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
            EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
            EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
