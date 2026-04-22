import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from battery_discharge import main_battery_discharge
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90]
unit = 0
channel_list = [1,2,3,4]
#1 Comms
#2 Vcoil
#3 Icoil
#4 Fsw

soak_time_per_line = 60
# OUTPUT
vout = 24
iout = 2.9
icoil_channel = 3

# PROJECT DETAILS
project = "DER-999"
excel_name = f"Unit {unit}, {vin_list[0]}Vac (FOD ADC)"
test = f"cmc/{vin_list[0]}Vac"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def CAPTURE_SCOPE_INSTANT(vin):
    global k
    CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
    vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
    scope.stop()
    vout = round(vout, 2)
    filename = f"{k} - DER-999 {vin} Vac, {vout} V, {CHARGING_CURRENT:.2f} A"
    path = waveforms_folder + f"\screenshots"
    GENERAL_FUNCTIONS().PATH_MAKER(path)
    # EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
    k+=1
    scope.run()

def main():
    global k
    k = 0
    scope.stop()
    
    EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

    # creating df header list
    header_list = GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_WIRELESS
    for channel in channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    for vin in vin_list:
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(10)

        scope.run()

        CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
        vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
        
        while (CHARGING_CURRENT < 0.5*iout):
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_WIRELESS(vin, vout, iout, channel_list)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="A1")
            CAPTURE_SCOPE_INSTANT(vin)
            soak(1)
            vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
            CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
            print("powering up...")

        for i in range(2):

            while (CHARGING_CURRENT > 0.1):
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_WIRELESS(vin, vout, iout, channel_list)
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="A1")
                CAPTURE_SCOPE_INSTANT(vin)
                soak(1)
                vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
                CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
                print("charging...")

            i = 0
            limit = 150
            while (i < limit):
                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_WIRELESS(vin, vout, iout, channel_list)
                
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="A1")
                CAPTURE_SCOPE_INSTANT(vin)
                soak(1)
                vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
                CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
                i+=1
                print(i)
                print(i*100/limit)
                print("last state")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().AC_TURN_OFF()


    # main_battery_discharge()

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
