# ======================================================================================
# DESCRIPTION
# ======================================================================================
# • Simple Efficiency vs Line Voltage
# • AC Source = [230, 265] VAC
# • Output Load = 2 A (CC)
# • Measures Pin (source power meter) and Pout (load power meter)
# • Computes Efficiency = Pout / Pin * 100
# ======================================================================================

import sys
import os
from datetime import datetime, timedelta
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

def soak_countdown(seconds, label="Soaking"):
    warning(f"{label} for {seconds} seconds...")
    for remaining in range(seconds, 0, -1):
        print(Fore.YELLOW + f"\r{label}: {remaining:4d} s remaining", end="", flush=True)
        sleep(1)
    print(Fore.YELLOW + f"\r{label}: DONE{' ' * 20}")

# ======================================================================================
# PARAMETERS
# ======================================================================================
vin_list    = [230, 265]        # AC source voltages (VAC)
iout        = 2                 # Output current (A) - CC load
soak_time   = 10                # Soak time per VIN step (seconds)

# ======================================================================================
# PROJECT INFO
# ======================================================================================
gf = GENERAL_FUNCTIONS()
dt_string   = gf.GET_DATE_STRING()
time_string = gf.GET_TIME_STRING()
username    = gf.GET_USERNAME()
test_name   = "Simple Efficiency"

ambient_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/DER/DER-1113/07 - Test Data/"
    f"{dt_string}/{test_name}/"
)
excel_name = f"DER-1113_Simple_Efficiency_{time_string}"

# ======================================================================================
def main():

    start_time = datetime.now()
    ef = EQUIPMENT_FUNCTIONS()

    # --- Header ---
    header_list = [
        'Vin (VAC)', 'Freq (Hz)',
        'Vac (rms)', 'Iin (mA)', 'Pin (W)', 'PF', '%THD',
        'Vout (V)', 'Iout (mA)', 'Pout (W)',
        'Efficiency (%)'
    ]
    df = gf.CREATE_DF_WITH_HEADER(header_list)

    # --- Set eload to 2 A CC and turn on ---
    ef.ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, iout)

    title(f"\n{'='*60}")
    title(f" DER-1113 Simple Efficiency Test")
    title(f" VIN = {vin_list} VAC  |  Iout = {iout} A")
    title(f"{'='*60}\n")

    for vin in vin_list:

        title(f"\n--- VIN = {vin} VAC ---")

        # Turn on AC source
        ef.AC_TURN_ON(vin)

        # Soak
        soak_countdown(soak_time, "Measurement Soak")

        # Measure input: Vac, Iin, Pin, PF, THD
        vac, iin, pin, pf, thd = ef._pm_measurements_source()

        # Measure output: Vout, Iout, Pout
        vout, iout_meas, pout = ef._pm_measurements1()

        # Compute efficiency
        try:
            eff = ef._sigfig(100 * pout / pin, 2)
        except:
            eff = "NaN"

        # Print results
        info(f"  Vac  = {vac} V")
        info(f"  Pin  = {pin} W")
        info(f"  Vout = {vout} V")
        info(f"  Iout = {iout_meas} mA")
        info(f"  Pout = {pout} W")
        success(f"  Efficiency = {eff} %")

        # Export to Excel
        freq = ac.set_freq(vin)
        export_to_excel(
            df,
            ambient_folder,
            [vin, freq, vac, iin, pin, pf, thd,
             vout, iout_meas, pout, eff],
            excel_name=excel_name,
            sheet_name=test_name,
            anchor="A1"
        )

    # --- Cleanup ---
    ef.DISCHARGE_OUTPUT(2)

    # --- Summary ---
    end_time = datetime.now()
    title(f"\n{'='*60}")
    title(f" TEST COMPLETE")
    title(f" Duration: {end_time - start_time}")
    title(f"{'='*60}\n")

# ======================================================================================
if __name__ == "__main__":
    headers(test_name)
    main()
    footers(waveform_counter)
    success(f"Results saved to:\n{ambient_folder}")
