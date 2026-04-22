import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

########################################## USER INPUT ##########################################
unit = 1
vin_list = [90, 100, 120, 132, 180, 200, 220, 230, 240, 265, 277]
vout = 1
cc = 1

# PROJECT DETAILS
project = "DER-867"
excel_name = f"Unit {unit}"
test = f"StdbyLk I_in"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################


def main():
    # creating df header list
    header_list = GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)
    
    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(60)
        pms.integrate(180)
        soak(180+2)
        output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, cc)
        export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="A1")

    # pms.reset()
    # pml.reset()

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
