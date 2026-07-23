
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
# vin_list = [90,100,110,115,120,132]
# vin_list = [132, 120, 115, 110, 100, 90]

# vin_list = [132,115,90]
vin_list = [132,115,90]

soak_time = 3
soak_time_per_line = 3
soak_time_per_load = 3

channel_to_trigger = 1
channel_trigger_delta = 1

percent_list = [100]
# port = "C1" # this is the port being measured
port = "C2" # this is the port being measured


# configuration = "Port 1 - 65W, Port 2 - NL"
# configuration = "Port 1 - NL, Port 2 - 65W"
# configuration = "Port 1 - 45W, Port 2 - 20W"
configuration = "Port 1 - 20W, Port 2 - 45W"



# PROJECT DETAILS
wavecapture_enabled = True
project = "DER-1024 Rev A"
test = f"Vds Ids Steady-State"
unit = 7
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/{test}/{configuration}/"
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################



def main():

    input("Press ENTER to turn on AC")

    print(configuration)
    if configuration == "Port 1 - 65W, Port 2 - NL":
        # print(configuration)
        load_list_1 = [(20,3.25)]
        load_list_2 = [(20,0)]
    elif configuration == "Port 1 - NL, Port 2 - 65W":
        load_list_1 = [(20,0)]
        load_list_2 = [(20,3.25)]
    elif configuration == "Port 1 - 45W, Port 2 - 20W":
        load_list_1 = [(20,2.25)]
        load_list_2 = [(20,1)]
    elif configuration == "Port 1 - 20W, Port 2 - 45W":
        load_list_1 = [(20,1)]
        load_list_2 = [(20,2.25)]
    else:
        pass


    for vout1, iout1 in load_list_1:
        for vout2, iout2 in load_list_2:

            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
            print(f"Set Port 1: {vout1}V/{iout1}A")
            print(f"Set Port 2: {vout2}V/{iout2}A")
            input(">> Press ENTER to continue... ")

            for vin in vin_list:
                
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
                cc_list_2 = [((iout2)*percent/100 if percent != 0 else 0) for percent in percent_list]
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc_list_2[0])

                
                scope.run()
                scope.trigger_mode(mode='AUTO')
                soak(1)
                scope.run_single()
                soak(1)

                filename = f"{test}_{vin}Vac_{port}_Port1_{vout1}V_{iout1}A_Port2_{vout2}V_{iout2}A"
                
                if wavecapture_enabled:
                    # EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=channel_to_trigger, trigger_delta=channel_trigger_delta)
                    prompt("Capture_waveform")
                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
