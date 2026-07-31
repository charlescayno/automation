from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90]

# PROJECT DETAILS
project = "DER-1015"
excel_name = f"Test"
test = f"Test"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(115)
    input()
    EQUIPMENT_FUNCTIONS().AC_TURN_OFF()
    
if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
