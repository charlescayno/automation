# ======================================================================================
# DESCRIPTION (UPDATED FLOW)
# ======================================================================================
# • Efficiency vs Line Voltage (Full Load Measurement)
# • Soak at Io = 2.89 A → 2 mins
# • Measure at Io = 15 A after 5 sec soak
# • VIN sweep: 180 → 230 → 265
# • Includes ETA, PASS/FAIL, margins, Excel export
# ======================================================================================

import sys
import os
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
# USER INPUT (unchanged)
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
    title("\nEnter unit ID:")
    unit_id = input("Unit ID: ").strip()
    if unit_id:
        unit_id = re.sub(r'[^A-Za-z0-9_-]', '_', unit_id); break
    error("Unit ID cannot be empty.")

# ======================================================================================
# PARAMETERS (UPDATED)
# ======================================================================================
vin_list = [180, 230, 265]

i_soak = 2.89      # soak current
i_test = 7      # measurement current
vout_nom = 28

soak_time_long = 120   # 2 minutes
soak_time_short = 5    # 5 seconds

PER_VIN_TIME = soak_time_long + soak_time_short
ESTIMATED_TOTAL_TIME = len(vin_list) * PER_VIN_TIME

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

test_name = "Eff vs Line PkPo"

ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

excel_name = f"{unit_id}_{ambient_temp}C_{time_string}"

# ======================================================================================
def main():

    start_time = datetime.now()
    estimated_end_time = start_time + timedelta(seconds=ESTIMATED_TOTAL_TIME)

    ef = EQUIPMENT_FUNCTIONS()

    header_list = [
        'Vin (VAC)', 'Vac', 'Iin', 'Pin',
        'Vout', 'Iout', 'Pout',
        'Efficiency (%)', 'Remark'
    ]

    df = gf.CREATE_DF_WITH_HEADER(header_list)

    # ✅ INITIAL ETA
    title(f"\nEstimated completion: {estimated_end_time.strftime('%H:%M:%S')}")

    for idx, vin in enumerate(tqdm(vin_list)):

        current_time = datetime.now()
        remaining_steps = len(vin_list) - idx
        eta = current_time + timedelta(seconds=remaining_steps * PER_VIN_TIME)

        title(f"\nVIN = {vin} VAC (ETA: {eta.strftime('%H:%M:%S')})")

        # --------------------------------------------------------------------------------
        # APPLY VIN
        # --------------------------------------------------------------------------------
        ef.AC_TURN_ON(vin)

        # --------------------------------------------------------------------------------
        # STEP 1: SOAK @ LIGHT LOAD (2.89A)
        # --------------------------------------------------------------------------------
        ef.MULTIPLE_ELOAD_CC_ON(0, 0, i_soak)
        soak_countdown(soak_time_long, "Soak @ 2.89A")

        # --------------------------------------------------------------------------------
        # STEP 2: FULL LOAD (15A) + SHORT SOAK
        # --------------------------------------------------------------------------------
        ef.MULTIPLE_ELOAD_CC_ON(0, 0, i_test)
        soak_countdown(soak_time_short, "Stabilize @ 15A")

        # --------------------------------------------------------------------------------
        # MEASUREMENT
        # --------------------------------------------------------------------------------
        vac, iin, pin, *_ = ef._pm_measurements()
        vout, iout, pout = ef._pm_measurements3()

        # --------------------------------------------------------------------------------
        # EFFICIENCY
        # --------------------------------------------------------------------------------
        try:
            eff = ef._sigfig(100 * pout / pin, 2)
        except:
            eff = "NaN"

        # --------------------------------------------------------------------------------
        # PASS/FAIL (91% criteria)
        # --------------------------------------------------------------------------------
        if isinstance(eff, (int, float)):
            margin = ef._sigfig(eff - 91, 2)
            if eff > 91:
                remark = f"PASS (+{margin}%)"
            else:
                remark = f"FAIL ({margin}%)"
        else:
            remark = "FAIL"

        info(f"Efficiency @15A: {eff}% → {remark}")

        # --------------------------------------------------------------------------------
        # EXPORT
        # --------------------------------------------------------------------------------
        export_to_excel(
            df,
            ambient_folder,
            [
                vin, vac, iin, pin,
                vout, iout, pout,
                eff, remark
            ],
            excel_name=excel_name,
            sheet_name=test_name,
            anchor="A1"
        )

    # ==================================================================================
    # FINAL SUMMARY
    # ==================================================================================
    title("\n================ FINAL SUMMARY ================")
    success("Test Completed")
    title("=============================================")

    ef.DISCHARGE_OUTPUT(2)

# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success("Saved successfully")
