from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

########################################## USER INPUT ##########################################
# INPUT
vin_list = [100]

icoil_channel = 3

# PROJECT DETAILS
project = "DER-999"
excel_name = "DER-999"
test = f"No Load"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    ac.coupling = 'DC'
    ac.voltage = 10
    ac.turn_on()
    soak(5)
    pms.integrate(5)
    soak(6)
    pin = EQUIPMENT_FUNCTIONS()._sigfig(pms.power, 6)
    soak(2)

if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)
