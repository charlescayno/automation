from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120,230]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30
soak_time = 1
soak_time_per_line = 1
soak_time_per_load = 1

# OUTPUT
iout = 3570

led_load_list = [36]
dim_list_final = [0, 2, 10]
on_time = 1
off_time = 1

# PROJECT DETAILS
project = "DER-1021"
test = f"AC Cycling"
unit = input(">> Enter unit number: ")
excel_name = f'{project}_{test}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():

    for led_load in led_load_list:
        EQUIPMENT_FUNCTIONS().LED_VOLTAGE(led_load)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        for vin in vin_list:


            for dim in dim_list_final:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=dim, current=0.1)
                scope.run_single()
                sleep(3)
                EQUIPMENT_FUNCTIONS().AC_CYCLING(3, vin, 3, on_time, on_time, 3)

                input("Capture waveform?")
                
                filename = f"{test}_{vin}VAC_{led_load}V_{dim}V"

                EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)