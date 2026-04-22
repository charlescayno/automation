## This is a normal operation code, set Vds at Ch2

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
# vin_list = [180, 200, 230, 240, 265]
vin_list = [180, 230, 265]

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6
pout_nom_1 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_1*iout_nom_1, 0)

vout_nom_2 = 24
iout_nom_2 = 2.4
pout_nom_2 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_2*iout_nom_2, 0)

vout_nom_3 = 5
iout_nom_3 = 0.5
pout_nom_3 = EQUIPMENT_FUNCTIONS()._sigfig(vout_nom_3*iout_nom_3, 0)

# PROJECT DETAILS
project = "DER-1050"
test = f"Pri Snub Optimization"
unit = "Rev A"

component = f"VDS"
voltage_rating = 750
# color = f"PINK"
# color = f"BLUE"
# color = f"GREEN"
# color = f"ORANGE"
color = f"YELLOW"
# color = f"GREEN"

# LIGHT_BLUE
# YELLOW
# PINK
# GREEN
# BLUE
# ORANGE


channel_to_trigger = 2
channel_trigger_delta = 2

wavecapture_enabled = True
excel_name = f'{component}'
waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{component}"
path = path_maker(f'{waveforms_folder}')
# waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():

    # EQUIPMENT_FUNCTIONS().SCOPE().RECALL_SAVESET('C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/PRIMARY_VDS_AND_FSW.dfl')
    # EQUIPMENT_FUNCTIONS().SCOPE().POSITION_SCALE(20, 10E-6)
    # EQUIPMENT_FUNCTIONS().SCOPE().CHANNEL_SETTINGS('ON', channel_to_trigger, 100, -4, component, color, 20, 500, 'DCLimit', 0)
    # EQUIPMENT_FUNCTIONS().SCOPE().CURSOR(channel_to_trigger, channel_to_trigger, X1=0, X2=0, Y1=0, Y2=0, type='VERT')
    input(">> Setup Scope. Place probe at Channel 2. Press ENTER to continue... ")
    
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_with_VDS_MAX[:])

    # EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=3, current=0.1)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        sleep(5)
        
        filename = f"{component}_{vin}Vac_{pout_nom_1+pout_nom_2+pout_nom_3}W_normal"

        if wavecapture_enabled:
            
            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(channel=channel_to_trigger, trigger_delta=channel_trigger_delta)
            EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
            # input(">> Find VDS max")


            vds_max = scope.get_measure_dict(channel_to_trigger)['Max']
            vdc = EQUIPMENT_FUNCTIONS()._sigfig(vin*1.414, 2)
            print(vds_max)
            print(vdc)
            sleep(1)
            scope.cursor(channel=2, cursor_set=1, X1=0, X2=0, Y1=vdc, Y2=vds_max, type='HOR')
            
            # input(">> Capture frequency ")

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_with_VDS_MAX(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, voltage_rating, channel_to_trigger)

            # EQUIPMENT_FUNCTIONS()
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{component}", anchor="A1")

            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
                
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)