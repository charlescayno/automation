from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,115,132]
vin_list = [90,132]

# soak_time = 300
# soak_time_per_line = 120
# soak_time_per_load = 30

soak_time = 30
soak_time_per_line = 5
soak_time_per_load = 5

# soak_time = 3
# soak_time_per_line = 3
# soak_time_per_load = 3


# OUTPUT
load_list_1 = [(15,3), (12,3), (9,3), (5,3)]
percent_list = range(100,-1,-1)
port = "C1"


channel_to_trigger = 1
channel_trigger_delta = 0.5

scope_channel_list = [1]

wavecapture_enabled = True
project = "DER-1024 Rev A"
test = f"Load Regulation with Ripple"
waveform = test
unit = 6
# datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/04 - Waveforms/01 - {test}/Unit {unit}"
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/Unit {unit}/Port {port}/"

# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################



def main():
    input("Press ENTER to turn on AC")
    # soak(5)
    

    i = 0
    for vout1, iout1 in load_list_1:

        create_header_for_df()
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        print(f"Set {port}: {vout1}V/{iout1}A")
        input("Set PD ports")
        
        c1 = EQUIPMENT_FUNCTIONS()._sigfig(vout1*iout1, 0)
        excel_name = f"{port}_{c1}W"
        
        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

            cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
            EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])
            
            if i == 0:
                print(f"soak input for {soak_time}s")
                soak(soak_time)
                i += 1
                    
            else:
                print(f"soak input for {soak_time_per_line}s")
                soak(soak_time_per_line)
                
            for io1 in cc_list:
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, io1)
                scope.run()
                scope.trigger_mode(mode='AUTO')
                print(f"soak per load for {soak_time_per_load}s")
                soak(soak_time_per_load)

                percent = EQUIPMENT_FUNCTIONS()._sigfig(io1*100/iout1, 0)
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL_SCOPE(vin, vout1, io1, percent, scope_channel_list)
                # print(output_list)
                # input()

                file_name = f"{excel_name}_{vout1}V{iout1}A"
                export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

                if wavecapture_enabled:
                    # EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=channel_to_trigger, trigger_delta=channel_trigger_delta)
                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(f"{waveform}_{vin}Vac_{vout1*io1}W_{vout1}V_{io1}A", path)

            output_list = EQUIPMENT_FUNCTIONS().BLANK_SPACE(df)
            export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

        i = 0

        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

        

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)



def create_header_for_df():
    global df
    """CREATING HEADER LIST"""
    header_list = GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_1[:]

    ## add header list for the scope
    # for channel in scope_channel_list:
    #     header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)

    header_list.append("Max")
    header_list.append("Pk-Pk")
    # header_list.append("C1 Y1")
    # header_list.append("C1 Y2")

    # create dataframe for the headerlist
    print("asdfsdf")
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)
    print(header_list)




if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
    # tts("Test Complete")
