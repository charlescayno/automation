from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [115, 230]
vin_list = [230]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_COMPARISON_CHECK
# OUTPUT
vout = 5
iout = 1
percent_list = [100]
cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]

# PROJECT DETAILS
project = "DER-991"
test = f"Power Check"

excel_name = test
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    count = 0
    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

        for cc in cc_list:
            percent = cc*100/iout
            if cc != 0: EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc)
            else: EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)

            soak(5)
            while 1:
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, cc)
                count += 1
                print(count, output_list)
                soak(1)



    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)

if __name__ == "__main__":
    # estimated_time =  len(vin_list)*soak_time_per_line
    # GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    headers(test)
    main()
    footers(waveform_counter)
