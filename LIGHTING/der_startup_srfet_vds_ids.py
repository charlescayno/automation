
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
# vin_list = [90,100,110,115,120,132]
# vin_list = [132, 120, 115, 110, 100, 90]
vin_list = [90,115,132]
# vin_list = [132,115,90]
# vin_list = [132]

soak_time = 7
soak_time_per_line = 7
soak_time_per_load = 7

load_list_1 = [(5,3)]
load_list_2 = [(5,0)]
percent_list = [100]
port = "C1" # this is the port being measured
# port = "C2" # this is the port being measured
configuration = "Port 1 - 15W, Port 2 - NL"
# configuration = "Port 1 - NL, Port 2 - 15W"
# configuration = "Port 1 - 15W, Port 2 - 15W"


# rel_pos = 80
# rel_scale = 0.02

# PROJECT DETAILS
wavecapture_enabled = True
project = "DER-1024 Rev A"
test = f"SR FET Vds Ids Startup"
unit = 7
datapath = f"C:/Users/ccayno/Documents/Charles/Work/DER/DER-1024 65W Dual Port/06 - Test Data/02 - ATE/{test}/{configuration}/"
waveforms_folder = path_maker(datapath)
########################################## USER INPUT ##########################################

def get_section_with_max_vds():
    # code to get the part where it is Vmax is located
    scope.remove_zoom_gate()
    # scope.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {10}")
    # scope.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {10}")
    # scope.add_zoom_gate()
    sleep(2)
    max_vds = scope.get_measure_dict(1)['Max']
    print(max_vds)
    sleep(1)
    scope.add_zoom_gate()
    sleep(1)

    scale = 10
    start_pos = 70
    while scale > rel_scale:
        for pos in np.arange(start_pos, 100, scale):
            scope.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {scale}")
            scope.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {pos}")
            sleep(0.5)
            current_vds = scope.get_measure_dict(1)['Max']
            if current_vds == max_vds:
                print(pos, scale, current_vds)
                scale = scale/2
                start_pos = pos-3*scale
                break

    for pos in np.arange(start_pos, 100, scale):
        scope.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {rel_scale}")
        scope.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {pos}")
        sleep(0.5)
        current_vds = scope.get_measure_dict(1)['Max']
        if current_vds == max_vds:
            print(pos, scale, current_vds)
            break

    scope.remove_zoom_gate()


def main():

    
    for vout1, iout1 in load_list_1:
        for vout2, iout2 in load_list_2:
            for vin in vin_list:            

                scope.run_single()

                cc_list = [((iout1)*percent/100 if percent != 0 else 0) for percent in percent_list]
                cc_list_2 = [((iout2)*percent/100 if percent != 0 else 0) for percent in percent_list]
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc_list[0])
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc_list_2[0])

                soak(2)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            
                soak(2)
                # scope.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {rel_scale}")
                # scope.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {rel_pos}")

                filename = f"{test}_{vin}Vac_{port}_Port1_{vout1}V_{iout1}A_Port2_{vout2}V_{iout2}A"

                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
                
                if wavecapture_enabled:
                    # get_section_with_max_vds()
                    
                    input("capture? ")
                    path = GENERAL_FUNCTIONS().PATH_MAKER(f"{waveforms_folder}")
                    EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
                

if __name__ == "__main__":
    headers(test)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)

    main()

    footers(waveform_counter)
