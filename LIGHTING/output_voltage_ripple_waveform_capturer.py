
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,110,115,120,132]
vin_list = [90,115,120,132]
vin_list = [90,132]

soak_time = 7
soak_time_per_line = 7
soak_time_per_load = 7


# OUTPUT
load_list_1 = [(5,3),(9,3),(12,3),(15,3),(20,3.25)]
# load_list_1 = [(9,3)]
# load_list_1 = [(12,3)]
# load_list_1 = [(15,3)]
# load_list_1 = [(20,3.25)]

# percent_list = [100,75,50,25,10,0]
percent_list = [100]
# percent_list = range(100,-2,-2)
port = "C1"
channel_to_trigger = 1
channel_trigger_delta = 0.001

# PROJECT DETAILS
wavecapture_enabled = True
project = "DER-1024 Rev B"
test = f"Output Ripple"
unit = input(">> Enter Unit Number: ")
# unit = "5"
excel_name = f'{project}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():
    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/der1024-ripple-waveform.dfl'")
    
    input("Press ENTER to turn on AC")

    for vout1, iout1 in load_list_1:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        print(f"Set {port}: {vout1}V")  
        input("Set PD ports")

        for vin in vin_list:
            
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

            cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
            EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])

            
            scope.run()
            scope.trigger_mode(mode='AUTO')
            soak(3)
            scope.run_single()
            soak(5)

            filename = f"{test}_{vin}Vac_{vout1}V_{iout1}A"

            if wavecapture_enabled:
                EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=channel_to_trigger, trigger_delta=channel_trigger_delta)
                path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
