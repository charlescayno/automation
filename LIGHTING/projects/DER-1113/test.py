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
slew_rate = 1  # V/s

# ✅ Fixed soak requirement
soak_time_fixed = 5  # seconds BEFORE and AFTER

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Brown In and Brown Out"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

# ===== FORMAT CURRENT =====
def format_current(iout):
    return str(iout).replace(".", "p")

# ===== LOGGER =====
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ===== TIME SCALE =====
def SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time):
    ramp_time = abs(stop_v - start_v) / slew_rate

    total_time = ramp_time + (2 * soak_time)

    time_scale = math.ceil(total_time / 10)
    total_scope_time = time_scale * 10

    print(f"\nRamp time: {ramp_time:.1f}s")
    print(f"Soak (before + after): {2 * soak_time}s")
    print(f"Total capture: {total_time:.1f}s")
    print(f"Setting scope to {time_scale} s/div")

    sc.TIME_SCALE(time_scale)

# ===== Brown-In =====
def BROWN_IN(ef):
    step = 1.0
    delay = max(0, (step / slew_rate) - 0.002)

    # ✅ 0 VAC soak first
    print(f"\n[BROWN-IN] 0 VAC soak for {soak_time_fixed}s")
    ef.AC_TURN_ON(start_v)
    sleep(soak_time_fixed)

    print(f"\nStarting Brown-In Ramp: {start_v} → {stop_v} VAC")

    vin = start_v
    while vin <= stop_v:
        ef.AC_TURN_ON(round(min(vin, stop_v), 2))
        log(f"[BROWN-IN] VIN = {vin:.2f} VAC")
        sleep(delay)
        vin += step

    # ✅ 180 VAC soak after
    print(f"\n[BROWN-IN] 180 VAC soak for {soak_time_fixed}s")
    sleep(soak_time_fixed)

# ===== Brown-Out =====
def BROWN_OUT(ef):
    step = 1.0
    delay = max(0, (step / slew_rate) - 0.002)

    # ✅ 180 VAC soak first
    print(f"\n[BROWN-OUT] 180 VAC soak for {soak_time_fixed}s")
    ef.AC_TURN_ON(stop_v)
    sleep(soak_time_fixed)

    print(f"\nStarting Brown-Out Ramp: {stop_v} → {start_v} VAC")

    vin = stop_v
    while vin >= start_v:
        ef.AC_TURN_ON(round(max(vin, start_v), 2))
        log(f"[BROWN-OUT] VIN = {vin:.2f} VAC")
        sleep(delay)
        vin -= step

    # ✅ 0 VAC soak after
    print(f"\n[BROWN-OUT] 0 VAC soak for {soak_time_fixed}s")
    sleep(soak_time_fixed)

# ===== MAIN =====
def main():

    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Use LONG memory depth on scope.")
    print("2. Set proper trigger for startup/dropout.")
    print("3. Setup Channel 1: Vout ripple probe (x10 passive).")
    print("4. Setup Channel 2: Vin differential probe (100:1).")
    print("===================================================================\n")

    input("\n✅ Setup complete? Press ENTER to start test...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    iout_str = format_current(iout)

    # ======================================================
    # ✅ BROWN-IN
    # ======================================================
    print("\n========== BROWN-IN CAPTURE ==========")

    ef.DISCHARGE_OUTPUT(2)
    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

    SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time_fixed)

    sc.RUN_SINGLE()
    sleep(2)

    try:
        BROWN_IN(ef)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted!")
        ef.AC_TURN_ON(0)
        ef.DISCHARGE_OUTPUT(2)
        return

    sc.STOP()

    brownin_filename = f"BrownIn_{start_v}to{stop_v}VAC_{iout_str}A"

    sc.SCOPE_SCREENSHOT(brownin_filename, save_folder)

    # ======================================================
    # ✅ BROWN-OUT
    # ======================================================
    print("\n========== BROWN-OUT CAPTURE ==========")
    

    ef.DISCHARGE_OUTPUT(2)
    sleep(2)

    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

    SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time_fixed)

    sc.RUN_SINGLE()
    sleep(2)

    try:
        BROWN_OUT(ef)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted!")
        ef.AC_TURN_ON(0)
        ef.DISCHARGE_OUTPUT(2)
        return

    sc.STOP()
    ef.DISCHARGE_OUTPUT(2)

    brownout_filename = f"BrownOut_{stop_v}to{start_v}VAC_{iout_str}A"

    sc.SCOPE_SCREENSHOT(brownout_filename, save_folder)

    print("\n✅ TEST COMPLETED\n")


if __name__ == "__main__":
    main()