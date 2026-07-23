from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from misc_codes.scope_setter import scope_settings
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180,200,230,265]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK
# OUTPUT
vout = 24
iout = 3
percent_list = [100] # percent_list = range(100, -1, -1) # 100% to 0% loading
cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]
# PROJECT DETAILS
# project = input(">> Project: ")
# excel_name = input(">> Excel Name: ")
# test = f"Waveforms - Vds Ids Steady-State"
# ########################################## USER INPUT ##########################################
# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)

# def main():
    
#     df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD)
    
#     row_counter = 2
#     for cc in cc_list:

#         EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
#         EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc)
#         EQUIPMENT_FUNCTIONS().AC_TURN_ON(180)
#         soak(3)

#         for vin in vin_list:

#             EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            
#             soak(soak_time_per_line)
            
#             scope.run_single()
#             soak(3)
#             EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=2, trigger_delta=1)
            
#             output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, cc)
#             export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

#             filename = f"Vds, Ids, Norm Op - {vin}Vac, {cc}A.png"
#             EQUIPMENT_FUNCTIONS().SCOPE_SCREENSHOT(filename=filename, path=waveforms_folder)
#             export_screenshot_to_excel(excel_name, waveforms_folder, excel_name, filename, f"Q{row_counter}")
#             row_counter += 34
            

#     GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
#     EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

        
if __name__ == "__main__":
    # estimated_time =  len(vin_list)*soak_time_per_line
    # GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    # headers(test)
    scope_settings()
    # main()
    # footers(waveform_counter)
