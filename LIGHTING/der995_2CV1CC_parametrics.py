from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [180, 200, 230, 240, 265]
# vin_list = [230]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30

# soak_time = 1
# soak_time_per_line = 1
# soak_time_per_load = 1

# OUTPUT
vout_nom_1 = 36
iout_nom_1 = 0.6

vout_nom_2 = 24
iout_nom_2 = 2.4

vout_nom_3 = 5
iout_nom_3 = 0.5


# PROJECT DETAILS
project = "DER-1050"
test = f"Final Board"
unit = f"RevD DisPS 2mH_diff_L"
excel_name = f'{project}_{unit}'

dt_string = GENERAL_FUNCTIONS().GET_DATE_STRING()
username = GENERAL_FUNCTIONS().GET_USERNAME()
waveforms_folder = f"C:/Users/{username}/Documents/Charles/Work/DER/{project}/5 - Test Data/{test}/{unit}/{dt_string}"
path = path_maker(f'{waveforms_folder}')
waveforms_folder = path

dim_freq = 10000
vds_channel = 4

########################################## USER INPUT ##########################################

def duty_list(start_duty, end_duty, delta_duty):
    if start_duty < end_duty:
        duty_list = np.arange(start_duty, end_duty+delta_duty, delta_duty)
    else: duty_list = np.arange(end_duty, start_duty-delta_duty, delta_duty)

    return duty_list

def main():
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/der995-iin.dfl'")
    # scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/der995-fsw-pf.dfl'")
    scope.write("MMEM:RCL 'C:/Users/Public/Documents/Rohde-Schwarz/RTx/SaveSets/2024/I_LED VDS I_CV2 FSW.dfl'")

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_2CV_1CC_PARAMETRICS[:])
    # EQUIPMENT_FUNCTIONS().SIG_GEN(99, dim_freq)

    EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
    sleep(2)

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    soak(soak_time)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().SCOPE().RUN()
        EQUIPMENT_FUNCTIONS().MULTIPLE_ELOAD_CC_ON(iout_nom_1, iout_nom_2, iout_nom_3)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        powerinput = EQUIPMENT_FUNCTIONS()._sigfig(pms.power, 2)
        filename = f"{vin}VAC {vout_nom_1}V{iout_nom_1}A {vout_nom_2}V{iout_nom_2}A {vout_nom_3}V{iout_nom_3}A PIN={powerinput}W"
        EQUIPMENT_FUNCTIONS().SCOPE().STOP()
        EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, waveforms_folder)

        output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_2CV_1CC_PARAMETRICS(vin, vout_nom_1, vout_nom_2, vout_nom_3, iout_nom_1, iout_nom_2, iout_nom_3, vds_channel)
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