import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)

from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import pandas as pd
import numpy as np

########################################## USER INPUT ##########################################
vin = 230
soak_time = 30  # soak time at nominal voltage before measurement

# Nominals
vout_nom_1 = 42
iout_nom_1 = 1.2
vout_nom_2 = 6
iout_nom_2 = 0.5
vout_nom_3 = 20
iout_nom_3 = 1.2

# PROJECT DETAILS
dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
time_string = GENERAL_FUNCTIONS().GET_TIME_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()

project_type = "DER"
project_name = "DER-1081"
results_folder = "07 - Test Data"
test_name = "Harmonics Measurement"
unit_no = "JW"
unit = f"Rev C Samples_{unit_no}"
excel_name = f'{unit_no}_Harmonics'

waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}/{results_folder}/{unit}/{test_name}/{dt_string}/"
path = path_maker(waveforms_folder)
waveforms_folder = path
################################################################################################

def get_harmonics_raw_data():
    """Queries the source power meter (pms) to retrieve the raw harmonics data array."""
    if pms is None:
        print("  [ERROR] Source Power Meter not connected!")
        return None
        
    try:
        idn = pms.write("*IDN?")
    except Exception as e:
        print(f"  [ERROR] Failed to query Power Meter: {e}")
        return None

    print(f"Power Meter IDN: {idn}")
    
    raw_data_str = ""
    if "WT210" in idn:
        print("Detected WT210. Reading harmonics...")
        pms.write("HARMONICS:STATE ON")
        pms.write("MEASURE:HARMONICS:ITEM:PRESET APATTERN")
        sleep(2)
        raw_data_str = pms.write("MEASURE:HARMONICS:VALUE?")
        pms.write("HARMONICS:STATE OFF")
        
    elif "WT310" in idn or "WT33" in idn:
        print("Detected WT310/WT300 series. Reading harmonics...")
        pms.write("HARMONICS:DISPLAY ON")
        pms.write("NUMERIC:LIST:CLEAR ALL")
        pms.write("NUMERIC:LIST:ITEM2 I,1")
        sleep(2)
        raw_data_str = pms.write("NUMeric:LIST:VALue? 2")
        pms.write("HARMONICS:STATE OFF")
        
    elif "Chroma" in idn:
        print("Detected Chroma Power Meter. Reading harmonics...")
        raw_data_str = pms.write("FETCH:CURRENT:HARMONIC:ARRAY? value")
        
    else:
        print("Unknown Power Meter model. Attempting generic harmonics query...")
        try:
            raw_data_str = pms.write("MEASURE:HARMONICS:VALUE?")
        except:
            try:
                raw_data_str = pms.write("NUMeric:LIST:VALue? 2")
            except Exception as e:
                print(f"Failed generic queries: {e}")
                return None
                
    if raw_data_str:
        # Convert comma-separated string to a list of floats
        try:
            raw_values = [float(x.strip()) for x in raw_data_str.split(',') if x.strip()]
            return raw_values
        except Exception as e:
            print(f"Error parsing raw harmonics string: {e}")
            return None
    return None

def process_harmonics_table(raw_values, pin, pf):
    """
    Applies standard Class C limits (EN61000-3-2) to the measured harmonics data.
    Limits are determined based on nominal Input Power (Pin):
      - Pin < 25W: limit in mA (absolute value)
      - Pin >= 25W: limit in % of fundamental
    """
    if not raw_values or len(raw_values) <= 2:
        print("Insufficient harmonics data to process.")
        return None
        
    # Fundamental (1st order) current is the reference (raw_values[2])
    iref_A = raw_values[2]
    iref_mA = iref_A * 1000.0
    
    rows = []
    
    # 1st harmonic
    rows.append({
        "nth order": 1,
        "mA content": round(iref_mA, 3),
        "% content": 100.00,
        "mA Limit <25W": "N/A",
        "% limit, >25W": "N/A",
        "Remarks": "Ref"
    })
    
    # 2nd harmonic
    if len(raw_values) > 3:
        i2_mA = raw_values[3] * 1000.0
        pct2 = (i2_mA / iref_mA) * 100.0 if iref_mA > 0 else 0
        rem2 = "pass"
        if pin >= 25.0:
            rem2 = "fail" if pct2 >= 2.0 else "pass"
        rows.append({
            "nth order": 2,
            "mA content": round(i2_mA, 3),
            "% content": round(pct2, 3),
            "mA Limit <25W": "N/A",
            "% limit, >25W": 2.0,
            "Remarks": rem2
        })
        
    # Odd harmonics: 3rd, 5th, 7th, 9th, 11th up to 39th
    for order in range(3, 41, 2):
        idx = order + 1  # 0-indexed offset: order 1 is at 2, order 2 is at 3, order 3 is at 4...
        if idx >= len(raw_values):
            break
            
        i_mA = raw_values[idx] * 1000.0
        pct = (i_mA / iref_mA) * 100.0 if iref_mA > 0 else 0
        
        # Determine Limits
        limit_mA = "N/A"
        limit_pct = "N/A"
        
        if order == 3:
            limit_mA = 3.4 * pin
            limit_pct = 30.0 * pf
        elif order == 5:
            limit_mA = 1.9 * pin
            limit_pct = 10.0
        elif order == 7:
            limit_mA = 1.0 * pin
            limit_pct = 7.0
        elif order == 9:
            limit_mA = 0.5 * pin
            limit_pct = 5.0
        elif order == 11:
            limit_mA = 0.35 * pin
            limit_pct = 3.0
        elif order > 11:
            limit_mA = (3.85 / order) * pin
            limit_pct = 3.0
            
        # Classify Pass/Fail
        remarks = "pass"
        if pin >= 25.0:
            if isinstance(limit_pct, (int, float)):
                remarks = "fail" if pct >= limit_pct else "pass"
        else:
            if isinstance(limit_mA, (int, float)):
                remarks = "fail" if i_mA >= limit_mA else "pass"
                
        rows.append({
            "nth order": order,
            "mA content": round(i_mA, 3),
            "% content": round(pct, 3),
            "mA Limit <25W": round(limit_mA, 3) if isinstance(limit_mA, (int, float)) else limit_mA,
            "% limit, >25W": round(limit_pct, 3) if isinstance(limit_pct, (int, float)) else limit_pct,
            "Remarks": remarks
        })
        
    return pd.DataFrame(rows)

def main():
    print("Initializing test...")
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    
    print(f"Soaking for {soak_time}s at {vin}VAC...")
    soak(soak_time)
    
    # Read nominal Input parameters
    print("Reading nominal line measurements...")
    vac, iin, pin, pf, thd, vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements()
    print(f"  Vin: {vac:.2f} V, Pin: {pin:.3f} W, PF: {pf:.4f}, THD: {thd:.2f}%")
    
    # Capture raw harmonics values
    raw_vals = get_harmonics_raw_data()
    
    if raw_vals:
        df_harm = process_harmonics_table(raw_vals, pin, pf)
        if df_harm is not None:
            print("\nHarmonics Analysis Table:")
            print(df_harm.to_string(index=False))
            
            # Export to Excel
            excel_path = os.path.join(waveforms_folder, f"{excel_name}.xlsx")
            with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
                df_harm.to_excel(writer, sheet_name="Harmonics_Table", index=False)
                
                # Write simple summary info at top of a Summary sheet
                summary_data = {
                    "Parameter": ["Vin (VAC)", "Pin (W)", "PF", "THD (%)", "Vo1 (V)", "Io1 (mA)", "Po1 (W)"],
                    "Value": [vac, pin, pf, thd, vo1, io1, po1]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name="Nominal_Summary", index=False)
                
            print(f"\n[SUCCESS] Harmonics table exported to: {excel_path}")
        else:
            print("[ERROR] Failed to process harmonics table.")
    else:
        print("[ERROR] Failed to capture raw harmonics data from Power Meter.")
        
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    headers(test_name)
    main()
    footers(0)
