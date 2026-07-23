# ======================================================================================
# DESCRIPTION
# ======================================================================================
# • Average Efficiency Test (DOE6)
# • VIN = [180, 230, 265]
# • Load sweep: 100%, 75%, 50%, 25%, 10%
# • Average uses: 100%, 75%, 50%, 25%
# • PASS if Avg Eff > 87.5%
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
ambient_temp = 25   # Fixed for simplicity (can reuse your selector if needed)

title("\nEnter unit ID:")
unit_id = input("Unit ID: ").strip()
unit_id = re.sub(r'[^A-Za-z0-9_-]', '_', unit_id)

# ======================================================================================
# PARAMETERS
# ======================================================================================
vin_list = [180, 230, 265]
load_percent_list = [100, 75, 50, 25, 10]

vout_nom = 28
iout_nom = 2.89

soak_time_start = 10
soak_time = 3

PER_POINT_TIME = soak_time_start + soak_time
ESTIMATED_TOTAL_TIME = len(vin_list) * len(load_percent_list) * PER_POINT_TIME

DOE_LIMIT = 87.5

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

test_name = "Average Efficiency DOE6"

ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/{ambient_temp}C/"
)

excel_name = f"{unit_id}_{ambient_temp}C_{time_string}"

# ======================================================================================
def main():

    start_time = datetime.now()
    estimated_end_time = start_time + timedelta(seconds=ESTIMATED_TOTAL_TIME)

    ef = EQUIPMENT_FUNCTIONS()

    header_list = [
        'Vin (VAC)', 'Load (%)',
        'Pin (W)', 'Pout (W)', 'Efficiency (%)'
    ]

    df = gf.CREATE_DF_WITH_HEADER(header_list)

    title(f"\nEstimated completion: {estimated_end_time.strftime('%H:%M:%S')}")

    overall_pass = True

    for vin in vin_list:

        title(f"\n===== VIN = {vin} VAC =====")

        ef.AC_TURN_ON(vin)

        eff_list_for_avg = []

        for load in load_percent_list:

            iout = iout_nom * load / 100
            ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout)

            soak_countdown(soak_time_start, "Initial Soak")
            soak_countdown(soak_time, "Measurement Soak")

            _, _, pin, _, _, *_ = ef._pm_measurements()
            _, _, pout = ef._pm_measurements3()

            try:
                eff = ef._sigfig(100 * pout / pin, 2)
            except:
                eff = "NaN"

            info(f"Load {load}% → Efficiency: {eff}%")

            # ✅ store for average (exclude 10%)
            if load != 10 and isinstance(eff, (int, float)):
                eff_list_for_avg.append(eff)

            export_to_excel(
                df,
                ambient_folder,
                [vin, load, pin, pout, eff],
                excel_name=excel_name,
                sheet_name=test_name,
                anchor="A1"
            )

        # ==================================================================================
        # AVERAGE CALCULATION
        # ==================================================================================
        if eff_list_for_avg:
            avg_eff = ef._sigfig(sum(eff_list_for_avg) / len(eff_list_for_avg), 2)
        else:
            avg_eff = "NaN"

        # ✅ PASS / FAIL
        if isinstance(avg_eff, (int, float)) and avg_eff > DOE_LIMIT:
            remark = f"PASS (+{ef._sigfig(avg_eff - DOE_LIMIT,2)}%)"
        else:
            remark = "FAIL"
            overall_pass = False

        title(f"\nVIN {vin} AVG Efficiency = {avg_eff}% → {remark}")

        export_to_excel(
            df,
            ambient_folder,
            ["", "AVG (100-25%)", "", "", avg_eff],
            excel_name=excel_name,
            sheet_name=test_name,
            anchor="H1"
        )

    # ==================================================================================
    # FINAL SUMMARY
    # ==================================================================================
    title("\n================ FINAL SUMMARY ================")

    if overall_pass:
        success("DOE6 Average Efficiency: PASS (>87.5%)")
    else:
        error("DOE6 Average Efficiency: FAIL")

    title("=============================================")

    ef.DISCHARGE_OUTPUT(2)

# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)