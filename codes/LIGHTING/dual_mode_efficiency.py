from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from powi.equipment import prompt
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 100, 110, 115, 120, 132]
vin_list = [90, 100, 115, 132]
vin_list = [115]

soak_time = 300
soak_time_per_line = 300
soak_time_per_load = 10

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1


# OUTPUT
load_list_1 = [(9,3)]
load_list_2 = [(9,3)]

port1 = "C1"
port2 = "C2"

percent_list_1 = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 0]
percent_list_2 = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 0]



project = "DER-1024 Rev A"
test = f"Dual Mode Efficiency (Port1 - {port1}, Port2 - {port2})"

unit = 6
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/{test}/"

waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################

def main():
    prompt("Press ENTER to turn on AC")

    i = 0
    for vout1, iout1 in load_list_1:
        for vout2, iout2 in load_list_2:

            df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_3[:])
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

            
            print(f"Set {port1}: {vout1}V/{iout1}A")
            print(f"Set {port2}: {vout2}V/{iout2}A")
            prompt("Set PD ports")
            
            c1 = EQUIPMENT_FUNCTIONS()._sigfig(vout1*iout1, 0)
            c2 = EQUIPMENT_FUNCTIONS()._sigfig(vout2*iout2, 0)
            excel_name = f"{c1+c2}W"
            print(excel_name)
            
            
            for vin in vin_list:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                
                cc_list_1 = [((iout1)*percent1/100 if percent1 != 0 else 0) for percent1 in percent_list_1]
                cc_list_2 = [((iout2)*percent2/100 if percent2 != 0 else 0) for percent2 in percent_list_2]

                for cc1 in cc_list_1:
                    for cc2 in cc_list_2:
                        
                        print(cc1, cc2)

                        EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc1)
                        EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc2)

                        if i == 0:
                            print(f"soak input for {soak_time}s")
                            soak(soak_time)
                            i += 1
                            
                        # else:
                        #     print(f"soak input for {soak_time_per_line}s")
                        #     soak(soak_time_per_line)
                        
                        soak(soak_time_per_load)

                        A = EQUIPMENT_FUNCTIONS()._sigfig(cc1*100/iout1, 0)
                        B = EQUIPMENT_FUNCTIONS()._sigfig(cc2*100/iout2, 0)

                        output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_DUAL_MODE_EFFICIENCY(vin, vout1, vout2, cc1, cc2, A, B)

                        export_to_excel(df, waveforms_folder, output_list, excel_name=f"{excel_name}_C1 {vout1}V{iout1}A_C2 {vout2}V{iout2}A", sheet_name=excel_name, anchor="A1")

                output_list = EQUIPMENT_FUNCTIONS().BLANK_SPACE(df)
                export_to_excel(df, waveforms_folder, output_list, excel_name=f"{excel_name}_C1 {vout1}V{iout1}A_C2 {vout2}V{iout2}A", sheet_name=excel_name, anchor="A1")

            i = 0
    
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

            

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
