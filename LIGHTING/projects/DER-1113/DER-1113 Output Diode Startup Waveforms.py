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

# Startup current levels
iout_list = [2.89, 7, 15]

vin_list = [180, 230, 265]

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Output Diode Startup Waveform"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

def main():

    # ===== USER REMINDERS (PROMPT ONLY ONCE) =====
    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Load the correct .DFL file into the oscilloscope.")
    print("2. Set Channel 1 to D7 (Output Diode).")
    print("3. Set Channel 2 to D5 (Output Diode).")
    print("===================================================================\n")

    input("Press ENTER once all setup steps are completed...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    for vin in vin_list:

        print(f"\n========== VIN = {vin} VAC ==========")

        for iout in iout_list:

            print(f"\nStartup Test at Io = {iout} A")

            filename = f"{vin}VAC_OutputDiode_Startup_Io_{iout}A"

            # 1. Discharge unit
            ef.DISCHARGE_OUTPUT(2)

            # 2. Set load current
            ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

            # 3. Scope single trigger
            sc.RUN_SINGLE()

            sleep(1)

            # 4. Turn ON AC (startup event)
            ef.AC_TURN_ON(vin)

            sleep(3)

            # 5. Discharge after capture
            ef.DISCHARGE_OUTPUT(2)

            # 6. Wait for user capture confirmation
            input("Capture waveform, then press ENTER to save...")

            # 7. Save waveform
            sc.STOP()
            sc.SCOPE_SCREENSHOT(filename, save_folder)

            sleep(1)

    print("\nTEST COMPLETED\n")


if __name__ == "__main__":
    main()