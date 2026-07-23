from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
# from powi.equipment import Arduino

########################################## USER INPUT ##########################################
# INPUT
vin_list = [90]
unit = 0

# PROJECT DETAILS
project = "Inno5_Pro"
excel_name = f"Debugger"
test = f"Debugger"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
def main():
    # soak(10)
    # EQUIPMENT_FUNCTIONS().AC_TURN_ON(150, 'DC')
    # soak(3)
    input()

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
