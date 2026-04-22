from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [132]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30

# OUTPUT
vout_nom_1 = 42
iout_nom_1 = 0.25

# PROJECT DETAILS
project = "TST-020"
test = f"Parametrics"
unit = "Julia"
excel_name = f'{project}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_COMPLETE[:])

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)


        vo2, io2, po2 = EQUIPMENT_FUNCTIONS()._pm_measurements2()
        vbulk = vo2
        i = 0

        while vbulk <= 450 and i < 30:

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_COMPLETE(vin, vout_nom_1, iout_nom_1, vbulk)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")

            soak(60*30)
            i = i + 1
                
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)