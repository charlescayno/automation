# ======================================================================================
# DESCRIPTION
# ======================================================================================
# • No Load Input Power
# • Integration-based measurement (mode dependent)
# • Adds remarks + summary PASS/FAIL
# • Shows ETA
# • Displays integration time in terminal
# • Operator prompt via ENTER
# ======================================================================================

import sys
import os
from datetime import datetime, timedelta
from time import sleep
import re

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.insert(0, os.path.join(_root, "Lib", "site-packages"))
sys.path.insert(0, _root)

from colorama import Fore, Style, init
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable=None, *args, **kwargs):
        return iterable if iterable is not None else range(kwargs.get('total', 0))

init(autoreset=True)

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
def soak(seconds):
    warning(f"Soaking for {seconds} seconds...")
    for remaining in range(seconds, 0, -1):
        print(Fore.YELLOW + f"\rSoaking: {remaining:4d} s remaining", end="", flush=True)
        sleep(1)
    print(Fore.YELLOW + f"\rSoaking: DONE{' ' * 20}")

# ======================================================================================
# ✅ Operator Prompt (ENTER)
# ======================================================================================
def prompt_no_load_config():
    title("\n================ OPERATOR ACTION REQUIRED ================")
    warning("Set DUT to NO LOAD CONFIGURATION")
    info("• Disconnect output load")
    info("• Ensure electronic load = 0 A")
    info("• Verify output is OPEN / No Load condition")
    title("==========================================================")

    input(Fore.YELLOW + "\nPress ENTER to continue once ready...")
    success("Configuration acknowledged.\n")

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
        test_mode = "NORMAL"
        soak_time_start = 120
        integration_time_seconds = 120   # ✅ NORMAL
        break

    elif choice == "2":
        test_mode = "FAST"
        soak_time_start = 5
        integration_time_seconds = 5   # ✅ FAST
        warning("FAST CHECK ENABLED")
        break

    error("Invalid selection.")

unit_id = os.environ.get("DUT_UNIT_ID", "").strip()
if not unit_id:
    while True:
        title("\nEnter unit ID:")
        unit_id = input("Unit ID: ").strip()
        if unit_id:
            break
        error("Unit ID cannot be empty.")
unit_id = re.sub(r'[^A-Za-z0-9_-]', '_', unit_id)

# ======================================================================================
# PARAMETERS
# ======================================================================================
vin_list = [180, 200, 220, 230, 240, 265]
vin_list = [180, 230, 265]
vin_list = [230]

PIN_LIMIT = 0.15  # Watts

PER_VIN_TIME = soak_time_start + integration_time_seconds + 5
ESTIMATED_TOTAL_TIME = len(vin_list) * PER_VIN_TIME

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

test_name = "No Load Input Power"

ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/"
)

excel_name = f"{unit_id}_{ambient_temp}C_{test_mode}_{time_string}"

# ======================================================================================
def main():

    start_time = datetime.now()
    estimated_end_time = start_time + timedelta(seconds=ESTIMATED_TOTAL_TIME)

    ef = EQUIPMENT_FUNCTIONS()

    # ✅ Operator prompt
    prompt_no_load_config()

    # ✅ Test conditions display
    title("\n================ TEST CONDITIONS ================")
    info(f"Test Name        : {test_name}")
    info(f"Integration Time : {integration_time_seconds} s")
    info(f"Vin Points       : {len(vin_list)}")
    info(f"Mode             : {test_mode}")
    title("================================================\n")

    header_list = [
        'Vin (VAC)', 'Freq (Hz)', 'Vac (rms)', 'Iin (A)',
        'Pin (W)', 'PF', '%THD',
        'Pin Remark'
    ]

    df = gf.CREATE_DF_WITH_HEADER(header_list)

    ef.MULTIPLE_ELOAD_CC_ON(0, 0, 0)

    all_pass = True

    title(f"\nEstimated completion time: {estimated_end_time.strftime('%H:%M:%S')}")

    for idx, vin in enumerate(tqdm(vin_list)):

        current_time = datetime.now()
        remaining_steps = len(vin_list) - idx
        remaining_time = remaining_steps * PER_VIN_TIME
        eta = current_time + timedelta(seconds=remaining_time)

        title(f"\nVIN = {vin} VAC | Integration = {integration_time_seconds}s (ETA: {eta.strftime('%H:%M:%S')})")

        ef.AC_TURN_ON(vin)

        soak(soak_time_start)

        # ✅ Integration
        pms.integrate(integration_time_seconds)
        soak(integration_time_seconds + 5)

        vac, iin, pin, pf, thd, *_ = ef._pm_measurements()

        try:
            pin_margin = ef._sigfig(PIN_LIMIT - pin, 3)
            if pin <= PIN_LIMIT:
                remark = f"PASS (+{pin_margin}W)"
            else:
                remark = f"FAIL ({pin_margin}W)"
                all_pass = False
        except:
            remark = "FAIL"
            all_pass = False

        info(f"Pin: {pin} W → {remark}")

        export_to_excel(
            df,
            ambient_folder,
            [
                vin, ac.set_freq(vin), vac, iin,
                pin, pf, thd,
                remark
            ],
            excel_name=excel_name,
            sheet_name=test_name,
            anchor="A1"
        )

    # ==================================================================================
    # FINAL SUMMARY
    # ==================================================================================
    title("\n================ FINAL SUMMARY ================")

    if all_pass:
        success(f"No Load Input Power: PASS (≤{PIN_LIMIT} W)")
    else:
        error("No Load Input Power: FAIL")

    title("=============================================")

    ef.DISCHARGE_OUTPUT(2)
    success("\nTEST COMPLETED\n")
    if not all_pass:
        sys.exit(1)

# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success(f"Saved to:\n{ambient_folder}")
