import sys
import os
from time import sleep
from datetime import datetime
import math

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.insert(0, os.path.join(_root, "Lib", "site-packages"))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# ===== USER CONFIGURATION =====
ambient_temp = 25
test_mode = "NORMAL"
unit_id = "RE_05"

# Brown parameters
iout = 2.89
start_v = 0
stop_v = 180
slew_rate = 10       # V/s (user adjustable)
soak_time = 10         # ✅ fixed

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Brown In and Brown Out"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

# ===== AUTO TIME SCALE (INTEGER ONLY) =====
def AUTO_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time):
    ramp_time = abs(stop_v - start_v) / slew_rate
    total_time = ramp_time + soak_time

    # ✅ round UP to whole number
    time_scale = math.ceil(total_time / 10)

    print(f"\nRamp time: {ramp_time:.1f}s")
    print(f"Soak time: {soak_time}s")
    print(f"Total capture time: {total_time:.1f}s")
    print(f"Setting scope time scale to {time_scale} s/div")

    sc.TIME_SCALE(time_scale)

# ===== Brown-In =====
def BROWN_IN(ef):
    step = 1.0
    delay = step / slew_rate

    print(f"\nStarting Brown-In: {start_v} → {stop_v} VAC @ {slew_rate} V/s")

    vin = start_v
    while vin <= stop_v:
        ef.AC_TURN_ON(round(vin, 2))
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [BROWN-IN] VIN = {vin:.2f} VAC")
        sleep(delay)
        vin += step

    # ✅ fixed soak AFTER ramp
    print(f"\n[BROWN-IN] Soaking at {stop_v} VAC for {soak_time}s")
    sleep(soak_time)

# ===== Brown-Out =====
def BROWN_OUT(ef):
    step = 1.0
    delay = step / slew_rate

    # ✅ fixed soak BEFORE ramp
    print(f"\n[BROWN-OUT] Soaking at {stop_v} VAC for {soak_time}s")
    sleep(soak_time)

    print(f"\nStarting Brown-Out: {stop_v} → {start_v} VAC @ {slew_rate} V/s")

    vin = stop_v
    while vin >= start_v:
        ef.AC_TURN_ON(round(vin, 2))
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [BROWN-OUT] VIN = {vin:.2f} VAC")
        sleep(delay)
        vin -= step

def main():

    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Use LONG memory depth on scope.")
    print("2. Set proper trigger for startup/dropout.")
    print("===================================================================\n")

    input("Press ENTER once setup is complete...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    # ======================================================
    # ✅ BROWN-IN CAPTURE
    # ======================================================
    print("\n========== BROWN-IN CAPTURE ==========")

    ef.DISCHARGE_OUTPUT(2)
    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

    AUTO_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time)

    sc.RUN_SINGLE()
    sleep(5)

    BROWN_IN(ef)

    sc.STOP()

    input("\nPress ENTER to save BROWN-IN waveform...")
    sc.SCOPE_SCREENSHOT("BrownIn_2p89A", save_folder)

    # ======================================================
    # ✅ BROWN-OUT CAPTURE
    # ======================================================
    print("\n========== BROWN-OUT CAPTURE ==========")

    ef.DISCHARGE_OUTPUT(2)
    sleep(2)

    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)
    ef.AC_TURN_ON(stop_v)
    sleep(2)

    AUTO_TIME_SCALE(sc, stop_v, start_v, slew_rate, soak_time)

    sc.RUN_SINGLE()
    sleep(3)

    BROWN_OUT(ef)

    sc.STOP()
    ef.DISCHARGE_OUTPUT(2)

    input("\nPress ENTER to save BROWN-OUT waveform...")
    sc.SCOPE_SCREENSHOT("BrownOut_2p89A", save_folder)

    print("\nTEST COMPLETED\n")


if __name__ == "__main__":
    main()