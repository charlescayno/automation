from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120,230]
vin_list = [230]

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1

# OUTPUT
led_load_list = [42, 36]
led_load_list = [42, 39, 36]
# led_load_list = [42]
dim_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
# dim_list = [5]s
# dim_list = [10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11]

vout_nom_1 = 36
iout_nom_1 = 3.57

vout_nom_2 = 6
iout_nom_2 = 0

vout_nom_3 = 12
iout_nom_3 = 0


# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER" # DER or APPS SUPPORT
project_name = "DER-1021"
results_folder = "Marketing Samples"
test_name = f"Startup At Different Dim"
unit = f"PH UNIT 1 PHTRF1 wR32"
excel_name = f'{unit}_{time_string}'


waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{dt_string}/{unit}/{test_name}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path
########################################## USER INPUT ##########################################


def main():

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)


    for led_load in led_load_list:

        input(f">> Change LED to {led_load}V")

        for dim in dim_list:

            EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(1, dim, 0.5)


            for vin in vin_list:

                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

                EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
                sleep(3)
                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                # input(">> Capture? ")

                sleep(5)

                # iout = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
                # iout_sig = EQUIPMENT_FUNCTIONS()._sigfig(iout*1000, 2)
                # filename = f"{vin}VAC, {led_load}V, Startup at Dim={dim}V, Iout={iout_sig}mA"

                filename = f"{vin}VAC, {led_load}V, Startup at Dim={dim}V"
                
                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
        
        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)
            

        

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)