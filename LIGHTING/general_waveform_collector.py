from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from misc_codes.scope_setter import scope_settings
from misc_codes.scope_config import *
########################################## USER INPUT ##########################################
project = "DER-991"
iteration = "UNIT 1"

test = f"SRFET VDS at Peak Load {iteration}"
iout = 1.5

vin_list = [90, 115, 230, 265]
vout_list = [20]

percent_list = [100]

filename = test
excel_name = test
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():

    cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    for vout in vout_list:
        for vin in vin_list:
            for cc in cc_list:
                # TURN ON E-LOAD
                percent = cc*100/iout
                if cc != 0: EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc)
                else: EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)

                # RUN SCOPE
                scope.run()
                soak(2)

                # TURN ON AC SOURCE
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                soak(3)
                # EQUIPMENT_FUNCTIONS().FIND_TRIGGER(1, 1)
                scope.run_single()
                soak(6)
                scope.stop()
                # input("Find max")
                # scope.stop()
                # input("Get fsw")
                

                # SAVE SCREENSHOT
                file_name = f"{filename}, {vin}Vac, {vout}V, {cc}A ({percent}%) Load"
                # file_name = f"{filename}, {vin}Vac, {vout}V"
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(file_name, waveforms_folder)
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)

