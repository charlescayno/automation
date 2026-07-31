import sys
import os
from time import sleep

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.insert(0, os.path.join(_root, "Lib", "site-packages"))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# ===== USER CONFIGURATION =====
ambient_temp = 25
test_mode = "NORMAL"
unit_id = "RE_05"

# Trigger settings (editable)
channel_to_trigger = 1
channel_trigger_delta = 3

# Test current levels
iout_list = [2.89, 7, 15]

# Input voltage levels
vin_list = [180, 230, 265]

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Output Diode Steady-state Waveform"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

def main():

    # ===== USER REMINDERS =====
    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Load the correct .DFL file into the oscilloscope.")
    print("2. Set Channel 1 to D7 (Output Diode).")
    print("3. Set Channel 2 to D5 (Output Diode).")
    print("===================================================================\n")

    input("Press ENTER once setup is complete...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    print(f"\nUsing Trigger Settings: Channel {channel_to_trigger}, Delta {channel_trigger_delta}")

    last_time_scale = None  # optimization

    for vin in vin_list:

        print(f"\n========== VIN = {vin} VAC ==========")

        for iout in iout_list:

            print(f"\nSteady-State Test at Io = {iout} A")

            filename = f"{vin}VAC_OutputDiode_SteadyState_Io_{iout}A"

            # 1. Set load current
            ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

            # 2. Turn ON AC
            ef.AC_TURN_ON(vin)

            # Allow system to reach steady-state
            sleep(1)

            # ===== Time scale control =====
            if iout >= 15:
                time_scale = 5e-6  # 5 us/div
                print("Setting time scale to 5 us/div (high load condition)")
            else:
                time_scale = 20e-6  # default (adjust if needed)

            # Apply only if changed
            if time_scale != last_time_scale:
                sc.TIME_SCALE(time_scale)
                last_time_scale = time_scale

            # 3. Find trigger
            ef.FIND_TRIGGER(
                channel=channel_to_trigger,
                trigger_delta=channel_trigger_delta
            )

            # 4. Capture waveform
            sc.RUN_SINGLE()
            sleep(1)
            sc.STOP()

            # 5. Discharge output AFTER capture
            ef.DISCHARGE_OUTPUT(2)

            # 6. User confirmation for saving
            input("Press ENTER to capture and save waveform...")

            # 7. Save waveform
            sc.SCOPE_SCREENSHOT(filename, save_folder)

            sleep(1)

    print("\nTEST COMPLETED\n")


if __name__ == "__main__":
    main()