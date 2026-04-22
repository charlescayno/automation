import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

########################################## USER INPUT ##########################################

# --- Test Mode ---
QUICK_CHECK = True  # Set to False for full DER soak times

# --- Input Voltage ---
vin_list = [195, 200, 230, 240, 265]

# --- Soak Times ---
if QUICK_CHECK:
    soak_time        = 5
    soak_time_per_line = 5
    soak_time_per_load = 5
else:
    soak_time        = 60
    soak_time_per_line = 30
    soak_time_per_load = 30

# --- Output Channels ---
vout_nom_1 = 12
iout_nom_1 = 1.2

vout_nom_2 = 6
iout_nom_2 = 0.5
iout2_list = [0.5, 0]

vout_nom_3 = 12
iout_nom_3 = 1.2

# --- Scope ---
scope_channel_list = [1, 2, 3]
scope_saveset_path = "C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2025/DER-1081/VDS VDS_SRFET V_DIODE STARTUP.dfl"

# --- Project Details ---
project_type   = "DER"          # "DER" or "APPS SUPPORT"
project_name   = "DER-1081"
results_folder = "07 - Test Data"
test_name      = "Startup Waveforms"
unit_no        = "1"
unit           = f"Rev C Samples_{unit_no}"
excel_name     = f"{unit_no}_{vout_nom_1}V"

username = GENERAL_FUNCTIONS().GET_USERNAME()
waveforms_folder = path_maker(
    f"C:/Users/{username}/Documents/Charles/Work/{project_type}/{project_name}"
    f"/{results_folder}/{unit}/{test_name}/{vout_nom_1}V"
)
print(f"Save path: {waveforms_folder}")

########################################## USER INPUT ##########################################


def main():
    eq = EQUIPMENT_FUNCTIONS()

    eq.SCOPE().RECALL_SAVESET(scope_saveset_path)

    header_list = GENERAL_CONSTANTS.HEADER_LIST_1CV_1CC_PARAMETRICS[:]
    for channel in scope_channel_list:
        header_list = eq.APPEND_SCOPE_LABELS(header_list, channel)
    print(header_list)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    eq.SCOPE().RUN()
    eq.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)

    for iout2 in iout2_list:
        for vin in vin_list:
            eq.SCOPE().RUN_SINGLE()
            eq.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout2, iout_nom_3)
            sleep(soak_time_per_load)
            eq.AC_TURN_ON(vin)
            soak(soak_time_per_line)

            filename = f"{test_name} {vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout2}A"
            eq.SCOPE().STOP()
            sleep(1)

            eq.SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

            output_list = eq.COLLECT_DATA_1CV_1CC_PARAMETRICS(
                vin, vout_nom_1, vout_nom_2, iout_nom_1, iout_nom_2, scope_channel_list
            )
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=test_name, anchor="A1")
            eq.DISCHARGE_OUTPUT(4)

        eq.DISCHARGE_OUTPUT(2)

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    eq.DISCHARGE_OUTPUT(2)


if __name__ == "__main__":
    eq = EQUIPMENT_FUNCTIONS()
    eq.DISCHARGE_OUTPUT(2)
    headers(test_name)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    eq.MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
