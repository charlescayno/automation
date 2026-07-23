# ======================================================================================
# DESCRIPTION
# ======================================================================================
# • Fully automated AC ON / AC OFF transient measurement for an offline LED driver PSU
# • Executes tests at both low-line (180 VAC) and high-line (265 VAC) input conditions
# • Applies a fixed constant-current load of 28 V / 2.89 A throughout the test
# • Allows user selection of ambient temperature: 25 °C or 60 °C
# • Supports two execution modes:
#     – Normal Check: full soak and timing for production validation
#     – Fast Check: reduced soak for debug and verification
# • User-selectable AC ON/OFF cycling:
#     – 500 ms ON / 500 ms OFF  → Scope 1 s/div
#     – 1 s ON / 1 s OFF        → Scope 2 s/div
# • Organizes data by ambient AND AC cycling mode
#
# Author        : Charles Michael Cayno
# Last Modified : 2026-04-29 (GMT+08)
# ======================================================================================

# ======================================================================================
# Imports and path setup
# ======================================================================================
import sys
import os
from time import sleep
from colorama import Fore, Style, init
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
# Soak countdown helper
# ======================================================================================
def soak_countdown(seconds, label):
    warning(f"{label} for {seconds} seconds...")
    for remaining in range(seconds, 0, -1):
        print(f"\r{label}: {remaining:4d} s remaining", end="", flush=True)
        sleep(1)
    print(f"\r{label}: DONE{' ' * 20}")

# ======================================================================================
# USER INPUT — AMBIENT
# ======================================================================================
while True:
    title("\nSelect ambient temperature for this test:")
    info("  [1] 25 °C")
    info("  [2] 60 °C")
    choice = input("Enter selection (1 or 2): ").strip()
    if choice == "1":
        ambient_temp = 25
        break
    elif choice == "2":
        ambient_temp = 60
        break
    error("Invalid selection.")

# ======================================================================================
# USER INPUT — TEST MODE
# ======================================================================================
while True:
    title("\nSelect test execution mode:")
    info("  [1] Normal Check")
    info("  [2] Fast Check")
    choice = input("Enter selection (1 or 2): ").strip()
    if choice == "1":
        soak_time_start = 8
        soak_time = 10
        break
    elif choice == "2":
        soak_time_start = 8
        soak_time = 10
        warning("FAST CHECK ENABLED")
        break
    error("Invalid selection.")

# ======================================================================================
# USER INPUT — AC CYCLING MODE
# ======================================================================================
while True:
    title("\nSelect AC ON/OFF cycling timing:")
    info("  [1] 500 ms ON / 500 ms OFF  (Scope: 1 s/div)")
    info("  [2] 1 s ON / 1 s OFF        (Scope: 2 s/div)")
    choice = input("Enter selection (1 or 2): ").strip()

    if choice == "1":
        CYCLING_ON_TIME  = 0.5
        CYCLING_OFF_TIME = 0.5
        SCOPE_TIME_DIV   = 1
        cycling_label    = "0.5s ON / 0.5s OFF"
        cycling_folder   = "0p5s_ON_0p5s_OFF"
        break
    elif choice == "2":
        CYCLING_ON_TIME  = 1.0
        CYCLING_OFF_TIME = 1.0
        SCOPE_TIME_DIV   = 2
        cycling_label    = "1s ON / 1s OFF"
        cycling_folder   = "1s_ON_1s_OFF"
        break
    error("Invalid selection.")

# ======================================================================================
# TEST PARAMETERS
# ======================================================================================
vin_list = [180, 265]
vout_nom = 28
iout_nom = 2.89

AC_STARTUP_SOAK = 3
AC_CYCLING_SOAK = 5
CYCLING_PULSE_COUNT = 5

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string   = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username    = gf.GET_USERNAME()

project_type   = "DER"
project_name   = "DER-1113"
test_name      = "AC ON-OFF Transient"
results_folder = "07 - Test Data"

unit       = f"{test_name}_{vout_nom}V"
excel_name = f"{unit}_{ambient_temp}C_{cycling_folder}_{time_string}"

# ✅ UPDATED: separate folder per AC cycling selection
ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/"
    f"{project_type}/{project_name}/{results_folder}/"
    f"{dt_string}/{unit}/{test_name}/"
    f"{ambient_temp}C/{cycling_folder}/"
)

# ======================================================================================
# MAIN TEST
# ======================================================================================
def main():

    ef = EQUIPMENT_FUNCTIONS()
    sc = ef.SCOPE()

    title("Loading oscilloscope setup...")
    sc.write(
        'MMEM:LOAD:SETUP '
        '"C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/der-1113/accycle.dfl"'
    )

    title(f"Setting scope timebase to {SCOPE_TIME_DIV} s/div")
    sc.write(f"TIMebase:SCALe {SCOPE_TIME_DIV}")

    ef.MULTIPLE_ELOAD_CC_ON(0, 0, iout_nom)

    for vin in vin_list:

        title(f"\n--- VIN = {vin} VAC ---")
        ef.AC_TURN_ON(vin)

        soak_countdown(AC_STARTUP_SOAK, "AC startup")
        soak_countdown(soak_time_start, "Initial soak")

        sc.STOP()
        sc.RUN_SINGLE()

        soak_countdown(soak_time, "Full-load soak")

        info(f"AC Cycling: {cycling_label}")

        for _ in range(CYCLING_PULSE_COUNT):
            ef.AC_TURN_OFF()
            sleep(CYCLING_OFF_TIME)
            ef.AC_TURN_ON(vin)
            sleep(CYCLING_ON_TIME)

        soak_countdown(AC_CYCLING_SOAK, "Post-cycling soak")

        input(">> Press ENTER if capture is okay.. ")
        success("Capture complete")

        sc.SCOPE_SCREENSHOT(
            f"{test_name}_{vin}VAC_{ambient_temp}C_{cycling_folder}",
            ambient_folder
        )

    ef.DISCHARGE_OUTPUT(2)
    success("\nALL TEST CONDITIONS COMPLETED\n")

# ======================================================================================
# ENTRY POINT
# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success(f"Saved results to:\n{ambient_folder}")