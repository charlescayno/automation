from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [265]

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

input(">> Press ENTER to discharge...")

EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    