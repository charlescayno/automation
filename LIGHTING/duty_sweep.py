from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
vin = 180
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5


EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

for i in range(0, 100, 10):
    if i == 0:
        EQUIPMENT_FUNCTIONS().SIG_GEN(0.002, 1000)
        # sleep(1)
    else:
        EQUIPMENT_FUNCTIONS().SIG_GEN(i, 1000)
        # sleep(0.01)
    # sleep(0.1)


sleep(10)