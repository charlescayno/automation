import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [230]

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

# PROJECT DETAILS
project = "DER-1050"
test = f"Power UP"
unit = "test"
excel_name = f'{project}_{unit}'

from datetime import datetime
now = datetime.now()
print("now =", now)
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
print("date and time =", dt_string)

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{dt_string}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path

dim_freq = 10000
vds_channel = 4

########################################## USER INPUT ##########################################
def main():
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    input(">> Press ENTER to discharge... ")
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)