from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [230]
vout = 12
iout = 1

eload_channel = 3

### 300 mW Efficiency
starting_iout_for_300mW = 0.0185 # A
iout_temp_delta_decrement = 0.0005 # A
soak_time_sec_per_load_300mW = 120
integration_time_sec_for_300mW_eff = 60

### NL PIN
nl_soak_time_sec = 120
nl_soak_time_sec_per_line = 10
nl_soak_time_sec_per_load = 5
nl_integration_time_sec = 60

# PROJECT DETAILS
# project = input(">> Enter project/DER name: ")
# unit = input(">> Input unit number/name: ")
iteration = input(">> Enter iteration: ")

test = f"300mW Eff and NL PIN"
project = "FAE Lab Challenge"
unit = 1


excel_name = f'{iteration}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_RBIAS_OPTIMIZATION[:])
    pms.reset()
    pml.reset()
    
    
    print("GETTING I_BIAS AND FL EFFICIENCY")
    input(">> Set switch to NL config, Set CH1 to Vbias, CH2 to Vbp")
    rbias = float(input(">> ENTER Rbias in kOhms: "))*1000
    # input(">> Press ENTER to turn on AC to get Ibias")

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    input("Set 300 mW in input power")
    # EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(eload_channel, iout)
    EQUIPMENT_FUNCTIONS().SCOPE().RUN()
    soak(5)

    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_RBIAS(vin_list[0], iteration, rbias)
    print(output_list)
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)


    # GETTING 300 mW efficiency
    print("\n\nGETTING 300mW EFFICIENCY")
    print(">> Set switch to NL config for 300 mW Efficiency")

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    # EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(eload_channel, starting_iout_for_300mW)
    iout_temp = starting_iout_for_300mW
    vac, iin, pin, pf, thd, vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements()

    # while pin < 0.3:
    #     iout_temp = iout_temp - iout_temp_delta_decrement
    #     EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(eload_channel, iout_temp)
    #     print(f"Soaking for {soak_time_sec_per_load_300mW}s ")
    #     soak(soak_time_sec_per_load_300mW)
    #     vac, iin, pin, pf, thd, vo1, io1, po1 = EQUIPMENT_FUNCTIONS()._pm_measurements()
    #     # pin = 0.3
    
    soak(soak_time_sec_per_load_300mW)
    print(f"Integrating input and output for {integration_time_sec_for_300mW_eff}s ")
    pms.integrate(integration_time_sec_for_300mW_eff)
    pml.integrate(integration_time_sec_for_300mW_eff)
    soak(integration_time_sec_for_300mW_eff+5)

    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_300mW_EFF(output_list)
    print(output_list)
    # EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)


    # GETTING NL input power
    print("\n\nGETTING NO LOAD INPUT POWER")
    input(">> Disconnect connectors for NL input power test")

    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])
    
    print(f"soak input for {nl_soak_time_sec}s")
    soak(nl_soak_time_sec)

    print(f"soak input for {nl_soak_time_sec_per_line}s")
    soak(nl_soak_time_sec_per_line)

    pms.integrate(nl_integration_time_sec)
    soak(nl_integration_time_sec+5)

    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_NL_after_300mW(output_list)
    print(output_list)
    file_name = f"{excel_name}"
    export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")


    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

        

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)

if __name__ == "__main__":
    headers(test)
    main()
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(3)
    footers(waveform_counter)
