# ======================================================================================
# Path setup to allow importing local project libraries
# ======================================================================================
import sys, os, re
from time import sleep
from datetime import datetime, timedelta

from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

# ======================================================================================
# COLOR PRINT HELPERS
# ======================================================================================
def title(msg): print(Fore.MAGENTA + Style.BRIGHT + msg)
def info(msg): print(Fore.CYAN + msg)
def success(msg): print(Fore.GREEN + msg)
def warning(msg): print(Fore.YELLOW + msg)
def error(msg): print(Fore.RED + msg)

# ======================================================================================
# USER INPUT
# ======================================================================================

while True:
    title("\nEnter unit ID:")
    unit_id = input("Unit ID: ").strip()
    if unit_id:
        unit_id = re.sub(r'[^A-Za-z0-9_-]', '_', unit_id)
        break
    error("Unit ID cannot be empty.")

while True:
    title("\nSelect ambient temperature:")
    info("  [1] 25 °C")
    info("  [2] 60 °C")

    ambient_choice = input("Enter selection (1 or 2): ").strip()

    if ambient_choice == "1":
        ambient_temp = 25
        break
    elif ambient_choice == "2":
        ambient_temp = 60
        break
    else:
        error("Invalid selection.")

while True:
    title("\nSelect soak mode:")
    info("  [1] Normal Test")
    info("  [2] Fast Check (Debug)")

    soak_choice = input("Enter selection (1 or 2): ").strip()

    if soak_choice == "1":
        soak_mode = "NORMAL"
        test_mode = "NORMAL"
        soak_time_start = 300
        soak_time = 10
        break

    elif soak_choice == "2":
        soak_mode = "FAST"
        test_mode = "FAST"
        soak_time_start = 1
        soak_time = 1
        warning("FAST CHECK MODE ENABLED — timings reduced!")
        break

    else:
        error("Invalid selection.")

vin_list = [180, 230, 265]

# ======================================================================================
# OUTPUT SETTINGS
# ======================================================================================
vout_nom_1 = 28
iout_nom_1 = 2.89
vout_nom_2 = 28
iout_nom_2 = 2.89
vout_nom_3 = 28
iout_nom_3 = 2.89

# ======================================================================================
# ✅ SCOPE SETTINGS (ADDED)
# ======================================================================================
scope_channel_list = [1, 2, 3]   # adjust as needed
scope_channel_labels = ["Vout", "Switch", "Current"]

# ✅ Trigger settings (ADDED)
channel_to_trigger = 1
channel_trigger_delta = 0.001

# ======================================================================================
# LOAD PROFILE
# ======================================================================================
load_points = 20
load_list = [
    round(iout_nom_3 * (load_points - 1 - i) / (load_points - 1), 3)
    for i in range(load_points)
]

# ======================================================================================
# PROJECT DETAILS
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username = gf.GET_USERNAME()

project_name = "DER-1113"
results_folder = "07 - Test Data"

test_name = "Line_Load_Reg"

excel_name = f"{unit_id}_{ambient_temp}C_{test_mode}_{time_string}"

# ======================================================================================
# ESTIMATED TIME
# ======================================================================================
def estimate_test_time():
    time_per_point = 2 + soak_time + 2
    time_per_vin = soak_time_start + len(load_list) * time_per_point
    total_time = len(vin_list) * time_per_vin
    return total_time

# ======================================================================================
# DATA FOLDER
# ======================================================================================
ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{unit_id}/{test_name}/{ambient_temp}C/"
)

# ======================================================================================
# MAIN TEST
# ======================================================================================
def main():

    est_time = estimate_test_time()

    start_time = datetime.now()
    est_end = start_time + timedelta(seconds=est_time)

    title("\n===================================================")
    title(f" STARTING TEST: {test_name}")
    info(f" Unit ID: {unit_id}")
    info(f" Ambient Temperature: {ambient_temp} °C")
    info(f" Mode: {test_mode}")
    info(f" Estimated Duration: {est_time/60:.1f} min")
    info(f" Estimated End Time: {est_end.strftime('%Y-%m-%d %H:%M:%S')}")
    title("===================================================\n")

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    input(Fore.YELLOW + ">> Verify setup, ENTER to start...")

    # ==================================================================================
    # ✅ HEADER CREATION (FIXED WITH SCOPE LABELS)
    # ==================================================================================
    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CC_LOAD3_PARAMETRICS[:]

    for ch in scope_channel_list:
        header_list = ef.APPEND_SCOPE_LABELS(
            header_list,
            ch,
            channel_labels=scope_channel_labels
        )

    df = gf.CREATE_DF_WITH_HEADER(header_list)

    ef.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, 0)

    for vin in vin_list:

        title(f"\n--- VIN = {vin} VAC ---")

        vin_folder = path_maker(os.path.join(ambient_folder, f"{vin}VAC"))

        ef.AC_TURN_ON(vin)
        ef.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

        soak(soak_time_start)

        with tqdm(total=len(load_list), desc=f"VIN {vin}") as pbar:

            for iout3 in load_list:

                load_percent = round((iout3 / iout_nom_3) * 100, 1)

                sc.RUN(); sleep(2)
                ef.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout3)

                # ✅ ORIGINAL
                soak(soak_time)

                # ✅ ✅ ADDED (your request)
                warning("    Soaking...")
                soak(soak_time)

                info("    Arming scope trigger...")
                ef.FIND_TRIGGER(channel_to_trigger, channel_trigger_delta)

                # ✅ CONTINUE ORIGINAL FLOW
                sc.RUN_SINGLE(); soak(2)

                filename = (
                    f"Line_Load_Reg_{vin}VAC_{ambient_temp}C_"
                    f"Load_{load_percent}pct.png"
                )

                sc.STOP()
                sc.SCOPE_SCREENSHOT(filename, vin_folder)

                output_list = ef.COLLECT_DATA_1CC_LOAD3_PARAMETRICS(
                    vin, vout_nom_3, iout_nom_3, scope_channel_list
                )

                # ✅ SAFETY CHECK (ADDED, no logic removed)
                if len(output_list) != len(df.columns):
                    error(f"Mismatch: {len(output_list)} vs {len(df.columns)}")
                    continue

                row_dict = dict(zip(df.columns, output_list))

                export_to_excel(
                    df, vin_folder, row_dict,
                    excel_name=excel_name,
                    sheet_name=test_name,
                    anchor="A1"
                )

                pbar.update(1)

    success("\nTEST COMPLETED")

# ======================================================================================
# RUN
# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success(f"Saved to:\n{ambient_folder}")