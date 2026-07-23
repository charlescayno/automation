from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import sys
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,110,115,120,132]
# vin_list = [110,115,120,132]
vin_list = [90,115,120,132]

soak_time_initial = 120
soak_time_per_line = 60
soak_time_per_load = 5

# soak_time_initial = 1
# soak_time_per_line = 1
# soak_time_per_load = 1



# OUTPUT

# load_list_1 = [(5,3)]
# load_list_1 = [(20,3.25),(15,3),(12,3),(9,3),(5,3)]
# load_list_1 = [(5,3)]
load_list_1 = [(20,3.25)]
# percent_list = [100,75,50,25,10]
# percent_list = [100]
percent_list = [100]
# percent_list = range(100, -5, -5)
# percent_list = range(100,-2,-2)
port = "C1"

# PROJECT DETAILS
project = "DER-1024 Rev A"

unit = input(">> Enter unit number: ")
test = f"Line Regulation"

# test = f"{port}_65W"
test = "Line Regulation"
# test = "Load Regulation"
# test = "Output Voltage Ripple"

# datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/{test}/"
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/XX - Marketing Samples/{test}/"

# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################

def main():
    input("Press ENTER to turn on AC")
    # soak(5)
    
    initial_soak = True
    initial_vin = vin_list[0]

    print()
    print(f"Initial Soak: {soak_time_initial}s")
    print(f"Soak per Line: {soak_time_per_line}s")
    print(f"Soak per Load: {soak_time_per_load}s")
    print()

    for vout1, iout1 in load_list_1:

        df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_PDEL[:])
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(initial_vin)
        # soak(5)
        # EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

        print(f"Set {port}: {vout1}V/{iout1}A")
        input("Set PD ports")
        
        c1 = EQUIPMENT_FUNCTIONS()._sigfig(vout1*iout1, 0)
        excel_name = f"{test}_{port}_{c1}W"
        
        
        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

            cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
            EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])
            
            if initial_soak:
                soak(soak_time_initial)
                initial_soak = False
                    
            else:
                soak(soak_time_per_line)
                
            for io1 in cc_list:

                scope.run()
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, io1)
                soak(soak_time_per_load)

                percent = EQUIPMENT_FUNCTIONS()._sigfig(io1*100/iout1, 0)
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL(vin, vout1, io1, percent)

                file_name = f"{unit}_{vout1}V{iout1}A"
                export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

            if len(percent_list) != 1:
                output_list = EQUIPMENT_FUNCTIONS().BLANK_SPACE(df)
                export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

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
