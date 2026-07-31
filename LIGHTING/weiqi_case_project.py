from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [110]

soak_time = 60
soak_time_per_line = 60
soak_time_per_load = 30

# OUTPUT
vout_nom_1 = 12
iout_nom_1 = 3

vout_nom_2 = 12
iout_nom_2 = 3

vout_nom_3 = 12
iout_nom_3 = 3


# PROJECT DETAILS
project = "Weiqi TOP266EG"
test = f"Test Data"
unit = f"TOP268EG"
vds_channel = 4
excel_name = f'{project}_{unit}'

dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()
waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/APPS SUPPORT/{project}/{test}/{unit}/{dt_string}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():
   

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(2)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().SCOPE().RUN()
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(3)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(30)
        
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(8.5, 8.5, 8.5)
        soak(30)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(3)
        soak(40)

        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(8.5, 8.5, 8.5)
        soak(30)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(3)
        soak(40)

        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(8.5, 8.5, 8.5)
        soak(30)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(3)
        soak(40)

        filename = f"{vin}VAC {vout_nom_1}V{iout_nom_1}A"
        
        input(">> Press ENTER to capture waveform...")
        EQUIPMENT_FUNCTIONS().SCOPE().STOP()
        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)