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
iout = 0
start_v = 0
stop_v = 180
slew_rate = 1  # V/s

# Fixed soak
soak_time_fixed = 5  # seconds

gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
username = gf.GET_USERNAME()

test_name = "Brown In and Brown Out"

save_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

# ===== HELPERS =====
def format_current(iout):
    return str(iout).replace(".", "p")

def format_slew(slew):
    return str(slew).replace(".", "p")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ===== 1-2-5 SCOPE ROUNDING =====
def round_to_scope_scale(value):
    base = [1, 2, 5]
    exponent = 0

    while True:
        for b in base:
            scaled = b * (10 ** exponent)
            if scaled >= value:
                return scaled
        exponent += 1

# ===== TIME SCALE =====
def SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time):
    ramp_time = abs(stop_v - start_v) / slew_rate
    total_time = ramp_time + (2 * soak_time)

    raw_scale = total_time / 10
    time_scale = round_to_scope_scale(raw_scale)

    total_scope_time = time_scale * 10
    extra_time = total_scope_time - total_time

    print(f"\nRamp time: {ramp_time:.1f}s")
    print(f"Soak (before + after): {2 * soak_time}s")
    print(f"Total waveform: {total_time:.1f}s")
    print(f"Scope scale: {time_scale} s/div")
    print(f"Total capture window: {total_scope_time:.1f}s")
    print(f"Extra margin: {extra_time:.1f}s")

    sc.TIME_SCALE(time_scale)

    return extra_time

# ===== BROWN-IN =====
def BROWN_IN(ef, extra_time):
    step = 1.0
    delay = max(0, (step / slew_rate) - 0.002)

    # ✅ EXTRA AT FRONT
    print(f"\n[BROWN-IN] Extra pre-trigger margin: {extra_time:.1f}s")
    sleep(extra_time)

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

    print(f"\n[BROWN-IN] 180 VAC soak for {soak_time_fixed}s")
    sleep(soak_time_fixed)

# ===== BROWN-OUT =====
def BROWN_OUT(ef, extra_time):
    step = 1.0
    delay = max(0, (step / slew_rate) - 0.002)

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

    print(f"\n[BROWN-OUT] 0 VAC soak for {soak_time_fixed}s")
    sleep(soak_time_fixed)

    # ✅ EXTRA AT END
    print(f"\n[BROWN-OUT] Extra tail margin: {extra_time:.1f}s")
    sleep(extra_time)

# ===== MAIN =====
def main():

    print("\n==================== IMPORTANT SETUP REMINDERS ====================")
    print("1. Use LONG memory depth on scope.")
    print("2. Set proper trigger for startup/dropout.")
    print("3. CH1: Vout ripple probe")
    print("4. CH2: Vin differential probe")
    print("===================================================================\n")

    input("\n✅ Setup complete? Press ENTER to start test...")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    iout_str = format_current(iout)
    slew_str = format_slew(slew_rate)

    # ======================================================
    # ✅ BROWN-IN
    # ======================================================
    print("\n========== BROWN-IN CAPTURE ==========")

    ef.DISCHARGE_OUTPUT(2)
    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

    extra_time = SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time_fixed)

    sc.RUN_SINGLE()
    sleep(2)

    try:
        BROWN_IN(ef, extra_time)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted!")
        ef.AC_TURN_ON(0)
        ef.DISCHARGE_OUTPUT(2)
        return

    sc.STOP()

    brownin_filename = f"BrownIn_{start_v}to{stop_v}VAC_{iout_str}A_SR{slew_str}Vps"
    sc.SCOPE_SCREENSHOT(brownin_filename, save_folder)

    # ======================================================
    # ✅ BROWN-OUT
    # ======================================================
    print("\n========== BROWN-OUT CAPTURE ==========")

    ef.DISCHARGE_OUTPUT(2)
    sleep(2)

    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

    extra_time = SET_TIME_SCALE(sc, start_v, stop_v, slew_rate, soak_time_fixed)

    sc.RUN_SINGLE()
    sleep(2)

    try:
        BROWN_OUT(ef, extra_time)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted!")
        ef.AC_TURN_ON(0)
        ef.DISCHARGE_OUTPUT(2)
        return

    sc.STOP()
    ef.DISCHARGE_OUTPUT(2)

    brownout_filename = f"BrownOut_{stop_v}to{start_v}VAC_{iout_str}A_SR{slew_str}Vps"
    sc.SCOPE_SCREENSHOT(brownout_filename, save_folder)

    print("\n✅ TEST COMPLETED\n")

if __name__ == "__main__":
    main()