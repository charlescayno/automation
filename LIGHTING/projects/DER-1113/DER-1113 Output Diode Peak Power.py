import sys
import os
from time import sleep

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.insert(0, os.path.join(_root, "Lib", "site-packages"))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

ambient_temp = 25
test_mode = "NORMAL"
unit_id = "RE_05"

iout_nom = 2.89
iout_step = 15

vin_list = [180, 230, 265]

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Output Diode Load Step Waveform"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

def main():

    # ===== USER REMINDERS =====
    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Load the correct .DFL file into the oscilloscope.")
    print("2. Channel 1 → Output Diode D7 waveform.")
    print("3. Channel 2 → Output Diode D5 waveform.")
    print("4. Channel 3 → Iout measurement.")
    print("===================================================================\n")

    input("Press ENTER once all setup steps are completed...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    for vin in vin_list:

        print(f"\nVIN = {vin} VAC")

        filename = f"{vin}VAC_D7_D5_Io_{iout_nom}A_to_{iout_step}A"

        # Set initial load and turn on AC
        ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout_nom)
        ef.AC_TURN_ON(vin)

        # Trigger scope
        sc.RUN_SINGLE()
        sleep(4)

        # Apply load step
        ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout_step)
        sleep(5)

        # Return to nominal load
        ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout_nom)

        input("Capture waveform, then press ENTER to save...")

        # Save waveform
        sc.STOP()
        sc.SCOPE_SCREENSHOT(filename, save_folder)

        # Discharge output for safety
        ef.DISCHARGE_OUTPUT(2)

    print("\nTEST COMPLETED\n")

if __name__ == "__main__":
    main()