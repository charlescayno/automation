from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 100, 115, 120, 230, 265]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_COMPARISON_CHECK
# OUTPUT
vout = 5
iout = 1
# PROJECT DETAILS
project = "DER-991"

test = f"SRFET Stress Startup (0107)"
test = f"Primary VDS Stress Startup (0107)"

excel_name = test
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    input(">> Set oscilloscope")

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, iout)
        scope.run_single()
        soak(2)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(2)
        scope.stop()
        # EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(f"{vin}Vac, {vout}V, {iout}A, SRFET Stress at Startup", waveforms_folder)
        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(f"{vin}Vac, {vout}V, {iout}A, Primary VDS Stress at Startup", waveforms_folder)
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)

if __name__ == "__main__":
    estimated_time =  len(vin_list)*soak_time_per_line
    GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    headers(test)
    main()
    footers(waveform_counter)
