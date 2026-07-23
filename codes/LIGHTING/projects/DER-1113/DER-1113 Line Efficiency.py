# ======================================================================================
# DESCRIPTION
# ======================================================================================
# • Efficiency + Vreg vs Line Voltage
# • Adds remarks + summary PASS/FAIL
# • Shows estimated completion time (ETA)
# • Includes margin in remarks
# ======================================================================================

import sys
import os
import time as time_module
from datetime import datetime, timedelta
from time import sleep
import re

from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.insert(0, os.path.join(_root, "Lib", "site-packages"))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# ======================================================================================
# Terminal helpers
# ======================================================================================
def title(msg):   print(Fore.MAGENTA + Style.BRIGHT + msg)
def info(msg):    print(Fore.CYAN + msg)
def success(msg): print(Fore.GREEN + msg)
def warning(msg): print(Fore.YELLOW + msg)
def error(msg):   print(Fore.RED + msg)

# ======================================================================================
def soak_countdown(seconds, label="Soaking"):
    warning(f"{label} for {seconds} seconds...")
    for remaining in range(seconds, 0, -1):
        print(Fore.YELLOW + f"\r{label}: {remaining:4d} s remaining", end="", flush=True)
        sleep(1)
    print(Fore.YELLOW + f"\r{label}: DONE{' ' * 20}")

# ======================================================================================
# USER INPUT
# ======================================================================================
while True:
    title("\nSelect ambient temperature:")
    info("[1] 25 °C")
    info("[2] 60 °C")
    choice = input("Enter selection: ").strip()
    if choice == "1":
        ambient_temp = 25; break
    elif choice == "2":
        ambient_temp = 60; break
    error("Invalid selection.")

while True:
    title("\nSelect test mode:")
    info("[1] Normal")
    info("[2] Fast")
    choice = input("Enter selection: ").strip()
    if choice == "1":
        test_mode = "NORMAL"; soak_time_start = 120; soak_time = 10; break
    elif choice == "2":
        test_mode = "FAST"; soak_time_start = 5; soak_time = 1
        warning("FAST CHECK ENABLED"); break
    error("Invalid selection.")

while True:
    title("\nEnter unit ID:")
    unit_id = input("Unit ID: ").strip()
    if unit_id:
        unit_id = re.sub(r'[^A-Za-z0-9_-]', '_', unit_id); break
    error("Unit ID cannot be empty.")

# ======================================================================================
# PARAMETERS
# ======================================================================================
vin_list = [180, 200, 220, 230, 240, 265]
vin_list = [230]
vout_nom = 28
iout_nom = 2.89

PER_VIN_TIME = soak_time_start + soak_time
ESTIMATED_TOTAL_TIME = len(vin_list) * PER_VIN_TIME

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

test_name = "Efficiency vs Line Voltage"

ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

# ✅ UPDATED HERE: Added test_mode to file name
excel_name = f"{unit_id}_{ambient_temp}C_{test_mode}_{time_string}"

# ======================================================================================
def main():

    start_time = datetime.now()
    estimated_end_time = start_time + timedelta(seconds=ESTIMATED_TOTAL_TIME)

    ef = EQUIPMENT_FUNCTIONS()

    # ✅ Headers (aligned to requirement)
    header_list = [
        'Vin (VAC)', 'Freq (Hz)', 'Vac (rms)', 'Iin (A)',
        'Pin (W)', 'PF', '%THD',
        'Vout (V)', 'Iout (A)', 'Pout (W)',
        'Vreg (%)', 'Efficiency (%)',
        'Eff Remark', 'Vreg Remark'
    ]

    df = gf.CREATE_DF_WITH_HEADER(header_list)
    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout_nom)

    all_eff_pass = True
    all_vreg_pass = True

    # ✅ Initial ETA display
    title(f"\nEstimated completion time: {estimated_end_time.strftime('%H:%M:%S')}")

    for idx, vin in enumerate(tqdm(vin_list)):

        # ✅ Dynamic ETA update
        current_time = datetime.now()
        remaining_steps = len(vin_list) - idx
        remaining_time = remaining_steps * PER_VIN_TIME
        eta = current_time + timedelta(seconds=remaining_time)

        title(f"\nVIN = {vin} VAC (ETA: {eta.strftime('%H:%M:%S')})")

        ef.AC_TURN_ON(vin)

        soak_countdown(soak_time_start, "Initial Soak")
        soak_countdown(soak_time, "Measurement Soak")

        vac, iin, pin, pf, thd, *_ = ef._pm_measurements()
        vout, iout, pout = ef._pm_measurements3()

        # ✅ VREG
        try:
            vreg = ef._sigfig(100 * (vout - vout_nom) / vout, 2)
        except:
            vreg = "NaN"

        # ✅ EFF
        try:
            eff = ef._sigfig(100 * pout / pin, 2)
        except:
            eff = "NaN"

        # ✅ Efficiency margin vs 91%
        if isinstance(eff, (int, float)):
            eff_margin = ef._sigfig(eff - 91, 2)
            if eff > 91:
                eff_remark = f"PASS (+{eff_margin}%)"
            else:
                eff_remark = f"FAIL ({eff_margin}%)"
                all_eff_pass = False
        else:
            eff_remark = "FAIL"
            all_eff_pass = False

        # ✅ Vreg margin vs ±5%
        if isinstance(vreg, (int, float)):
            vreg_margin = ef._sigfig(5 - abs(vreg), 2)
            if -5 <= vreg <= 5:
                vreg_remark = f"PASS (Margin: {vreg_margin}%)"
            else:
                vreg_remark = f"FAIL ({vreg_margin}%)"
                all_vreg_pass = False
        else:
            vreg_remark = "FAIL"
            all_vreg_pass = False

        # ✅ Terminal output
        info(f"Efficiency: {eff}% → {eff_remark}")
        info(f"Vreg      : {vreg}% → {vreg_remark}")

        # ✅ Export to Excel
        export_to_excel(
            df,
            ambient_folder,
            [
                vin, ac.set_freq(vin), vac, iin, pin, pf, thd,
                vout, iout, pout, vreg, eff,
                eff_remark, vreg_remark
            ],
            excel_name=excel_name,
            sheet_name=test_name,
            anchor="A1"
        )

    # ==================================================================================
    # FINAL SUMMARY
    # ==================================================================================
    title("\n================ FINAL SUMMARY ================")

    if all_eff_pass:
        success("Efficiency: PASS (>91% all VIN)")
    else:
        error("Efficiency: FAIL")

    if all_vreg_pass:
        success("Vreg: PASS (-5% to 5%)")
    else:
        error("Vreg: FAIL")

    title("=============================================")

    ef.DISCHARGE_OUTPUT(2)
    success("\nTEST COMPLETED\n")

# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success(f"Saved to:\n{ambient_folder}")
