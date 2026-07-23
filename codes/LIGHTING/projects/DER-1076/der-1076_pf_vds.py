import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from datetime import datetime
now = datetime.now()
print("now =", now)
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
print("date and time =", dt_string)
folder = dt_string
########################################## USER INPUT ##########################################
# soak_time = 300
# soak_time_per_line = 120
# soak_time_per_load = 30

soak_time = 5
soak_time_per_line = 5
soak_time_per_load = 5

# OUTPUT
vout_nom_1 = 24
iout_nom_1 = 1.7

vout_nom_2 = 0
iout_nom_2 = 0

vout_nom_3 = 0
iout_nom_3 = 0

# PROJECT DETAILS
project = "DER-1076"
test = f"PF THD VDS"
unit = f"1"
# unit = f"test"

excel_name = f'PFvsCV1_{dt_string}'
vin_list = [230]
iout_list = [0, 1.7] # CV1 sweep

# excel_name = f'PFvsLine_{dt_string}'
# vin_list = [180, 200, 230, 240, 265]
# iout_list_CV1 = [0.5] # CV1 sweep

# # iout_list_CV2 = [0, 0.1042*0.25, 0.1042*0.5, 0.1042*0.75, 0.1042]

iout_list_CV2 = [0]

waveforms_folder = f"C:/Users/ccayno/Documents/Charles/Work/DER/{project}/2 - Test Data/{test}/{unit}/{excel_name}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path

dim_freq = 10000
vds_channel = 2
iled_channel = 1
########################################## USER INPUT ##########################################
def main():
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/I_LED VDS I_CV2 FSW.dfl'")

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_1CC[:])
    sleep(2)
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    
    soak(soak_time)

    for vin in vin_list:
        for iout in iout_list:

            EQUIPMENT_FUNCTIONS().SCOPE().RUN()
            EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout, iout_nom_2, iout_nom_3)
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
            soak(soak_time_per_line)

            EQUIPMENT_FUNCTIONS().FIND_TRIGGER(2, 1)

            powerinput = EQUIPMENT_FUNCTIONS()._sigfig(pms.power, 2)
            powerfactor = EQUIPMENT_FUNCTIONS()._sigfig(pms.pf, 3)

            filename = f"{vin}VAC {vout_nom_1}V{iout}A SVF enabled PIN={powerinput}W PF={powerfactor}"
            EQUIPMENT_FUNCTIONS().SCOPE().STOP()
            EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_1CC(vin, vout_nom_1, iout, vds_channel)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=f"{test}", anchor="A1")
                    
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)



if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)
    print(f"Data saved at folder:\n\n {waveforms_folder}\n\n")
    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)