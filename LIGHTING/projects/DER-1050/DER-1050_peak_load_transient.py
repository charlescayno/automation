import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 230, 265]
vin_list = [230]

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5


# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5

load_increment_1 = 10

# PROJECT DETAILS
project = "DER-1050"
test = f"Peak Load Transient"
unit = "Rev B"
excel_name = f'{project}_{unit}'

from datetime import datetime
now = datetime.now()
print("now =", now)
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
print("date and time =", dt_string)

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path


dim_freq = 10000
########################################## USER INPUT ##########################################

def ENABLE_DIMMING():
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, 1000)





def main():


    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    
    EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

    for vin in vin_list:

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        
        EQUIPMENT_FUNCTIONS().SCOPE().RUN_SINGLE()
        input(">> Proceed to peak load? ")
        iout_nom_2_peak = 5.8
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2_peak, iout_nom_3)
        
        sleep(2)
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)


        input(">> Capture screenshot? ")
        iterno = "SRFET - Layout 41 - Trim Option 2"
        filename = f"iteration {iterno}_{vin}Vac_CV2_{iout_nom_2}A_to_{iout_nom_2_peak}A"
        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)

        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    