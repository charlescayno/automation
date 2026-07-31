from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import numpy as np
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180,264]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_DER
# soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK
# OUTPUT
vout = 59
iout = 3.93
iout_nom = 2
percent_list = range(0, 101, 1) # 0% to 100% loading

project = "DER-580 CVCC Curve Modification"
test = f"CVCC using CV mode"
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
cv_list = np.arange(55, 58.5, 0.5)

def main():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CR_LOAD)

    scope.stop()
    soak(2)
    
    for vin in vin_list:
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

        soak(5)
        scope.run()
        soak(3)

        for cv in cv_list:
            EQUIPMENT_FUNCTIONS().ELOAD_CV_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cv)

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CV_LOAD(vin, vout, iout_nom, cv)
            excel_name = f"{vin}Vac, CVCC at CV mode"
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

            print(output_list)
            soak(3)
            
        GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
        scope.stop()
        EQUIPMENT_FUNCTIONS().SCOPE_SCREENSHOT(f"{excel_name}.png", waveforms_folder)

    for i in range(3):
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
    main()

