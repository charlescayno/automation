from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_DER
# soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK
# OUTPUT
vout = 59
iout = 3.93
percent_list = range(0, 101, 1) # 0% to 100% loading

project = "DER-580 CVCC Curve Modification"
# excel_name = input(">> Enter excel name: ")
test = f"CVCC"
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]
cr_list = [(vout/(iout*(percent/100)) if percent != 0 else 0) for percent in percent_list]

def main():

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    scope.stop()
    soak(2)

    for vin in vin_list:
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

        soak(5)
        scope.run()
        soak(3)

        for cr in cr_list:

            if cr != 0: EQUIPMENT_FUNCTIONS().ELOAD_CR_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cr, 0)
            else: EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CR_LOAD(vin, vout, cr)
            excel_name = f"{vin}Vac, CVCC"
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

            print(output_list)
            soak(3)

        GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
        scope.stop()
        EQUIPMENT_FUNCTIONS().SCOPE_SCREENSHOT(f"{excel_name}", waveforms_folder)

        for i in range(3):
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CR_LOAD)
    main()

