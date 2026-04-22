from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 100, 115, 120, 230, 265]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_COMPARISON_CHECK
# OUTPUT
vout = 20
iout = 1.5
percent_list = [100, 75, 50, 25, 10, 5, 0]
cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]

# PROJECT DETAILS
project = "DER-991"
test = f"Vout Ripple (Vout = {vout}V)"

excel_name = test
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

        for cc in cc_list:
            percent = cc*100/iout
            if cc != 0: EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc, 0)
            else: EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)

            soak(5)

            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(1, 0.01)

            scope.run_single()
            soak(3)
            scope.stop()

            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(f"{vin}Vac, {vout}V, {cc}A, {percent}% Load, VoRipple", waveforms_folder)
        
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)

if __name__ == "__main__":
    estimated_time =  len(vin_list)*soak_time_per_line
    GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    headers(test)
    main()
    footers(waveform_counter)
