
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
# vin_list = [90,100,110,115,120,132]
# vin_list = [132, 120, 115, 110, 100, 90]
vin_list = [132,115,90]
# vin_list = [90]

soak_time = 7
soak_time_per_line = 7
soak_time_per_load = 7

load_list_1 = [(5,3)]
load_list_2 = [(5,3)]
percent_list = [100]
port = "C1" # this is the port being measured
# port = "C2" # this is the port being measured
# configuration = "Port 1 - 15W, Port 2 - NL"
# configuration = "Port 1 - NL, Port 2 - 15W"
configuration = "Port 1 - 15W, Port 2 - 15W"



rel_scale = 0.02

# PROJECT DETAILS
wavecapture_enabled = True
project = "DER-1024 Rev A"
test = f"Vds Ids Startup"
unit = 7
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/{test}/{configuration}/"
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################

def get_section_with_max_vds():

    scope.remove_zoom_gate()
    sleep(2)
    max_vds = scope.get_measure_dict(1)['Max']
    print(f"Maximum Vds = {max_vds} V")
    sleep(1)
    scope.add_zoom_gate()
    sleep(1)

    scale = 10
    start_pos = 5
    end_pos = 50
    while scale > rel_scale:
        for pos in np.arange(start_pos, end_pos+5, scale):
            EQUIPMENT_FUNCTIONS().SCOPE().ADJUST_ZOOM_SCALE_POS(scale, pos)
            sleep(0.5)
            current_vds = scope.get_measure_dict(1)['Max']
            if current_vds == max_vds:
                print(pos, scale, current_vds)
                new_pos = pos
                new_scale = scale/10
        
            new_pos = 35
            new_scale = 1

            adjusted_pos = (new_pos - scale/2) + new_scale/2
            print(adjusted_pos)

        for pos in np.arange(adjusted_pos, adjusted_pos+10*new_scale, new_scale):
            print(pos, new_scale)
            EQUIPMENT_FUNCTIONS().SCOPE().ADJUST_ZOOM_SCALE_POS(new_scale, pos)
            sleep(0.5)
            current_vds = scope.get_measure_dict(1)['Max']
            if current_vds == max_vds:
                print(pos, new_scale, current_vds)
                new_pos = pos
                new_scale = new_scale/10

        for pos in np.arange(new_pos-5, new_pos+5, scale):
            EQUIPMENT_FUNCTIONS().SCOPE().ADJUST_ZOOM_SCALE_POS(scale, pos)
            sleep(0.5)
            current_vds = scope.get_measure_dict(1)['Max']
            if current_vds == max_vds:
                print(pos, scale, current_vds)
                new_pos = pos
                scale = scale/10
            input()

    # for pos in np.arange(start_pos, 100, scale):
    #     EQUIPMENT_FUNCTIONS().SCOPE().ADJUST_ZOOM_SCALE_POS(rel_scale, pos)
    #     sleep(0.5)
    #     current_vds = scope.get_measure_dict(1)['Max']
    #     if current_vds == max_vds:
    #         print(pos, scale, current_vds)
    #         break

    scope.remove_zoom_gate()


def main():

    
    for vout1, iout1 in load_list_1:
        for vout2, iout2 in load_list_2:
            for vin in vin_list:            

                EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()

                cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
                cc_list_2 = [((iout2)*percent/100 if percent != 0 else 0) for percent in percent_list]
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc_list_2[0])

                soak(2)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            
                soak(2)

                filename = f"{test}_{vin}Vac_{port}_Port1_{vout1}V_{iout1}A_Port2_{vout2}V_{iout2}A"

                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
                
                if wavecapture_enabled:
                    # get_section_with_max_vds()
                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                    input("Capture waveform?")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
                

if __name__ == "__main__":
    headers(test)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)

    main()

    footers(waveform_counter)
