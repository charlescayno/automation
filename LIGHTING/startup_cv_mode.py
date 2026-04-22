from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import numpy as np
########################################## USER INPUT ##########################################
# INPUT
vin_list = [264]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_DER
# soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_QUICK_CHECK
# OUTPUT
vout = 59
iout = 3.93
iout_nom = 2
percent_list = range(0, 101, 1) # 0% to 100% loading

project = "DER-580 CVCC Curve Modification"
test = f"CV mode startup"
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################
cv_list = [40,35,34,33,32,31,30]
cv_list = [34.5]

def main():

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
        scope.stop()
        soak(3)
        for cv in cv_list:

            scope.run_single()
            soak(3)
        
            EQUIPMENT_FUNCTIONS().ELOAD_CV_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cv)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

            soak(11)
            
            scope.stop()
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(f"{vin}Vac, CV={cv}V, startup", waveforms_folder)
            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
    main()

