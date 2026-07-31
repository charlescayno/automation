from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import sys
########################################## USER INPUT ##########################################
# led_load = float(input(">> LED voltage (V): "))
# vin = float(input(">> Input Voltage (VAC): "))
led_load = float(sys.argv[1])
vin = float(sys.argv[2])
########################################## USER INPUT ##########################################

def main():
    EQUIPMENT_FUNCTIONS().LED_VOLTAGE(led_load)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
    input(">> Press ENTER to end..")
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)

if __name__ == "__main__":
    main()