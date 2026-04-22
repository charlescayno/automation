from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
from battery_discharge import main_battery_discharge
import numpy as np
########################################## USER INPUT ##########################################
# INPUT
vin = [90]

start = 90
end = 132
slew = 0.5
frequency = 60

unit = 1

soak_time_per_line = 60
# OUTPUT
vout = 24
iout = 2.9
icoil_channel = 3

# PROJECT DETAILS
project = "DER-999"
# test = f"Line Transient Up"
test = f"Brown in Retest"
excel_name = f"{project} {test}"
channel_list=[2,3,4] # select channels to capture data, 2-Vsense, 3-Icoil, 4-PWM

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def CAPTURE_SCOPE_INSTANT(vin):
    global k
    CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
    OUTPUT_VOLTAGE = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
    scope.stop()
    OUTPUT_VOLTAGE = round(OUTPUT_VOLTAGE, 2)
    filename = f"{k} - {vin} Vac, {OUTPUT_VOLTAGE} V, {CHARGING_CURRENT:.2f} A"
    path = waveforms_folder + f"\screenshots"
    # EQUIPMENT_FUNCTIONS().SCOPE().SCOPE_SCREENSHOT(filename, path)
    k+=1
    scope.run()

def CAPTURE_DATA(vin, df, excel_name):
    CAPTURE_SCOPE_INSTANT(vin)
    output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_BROWNIN_WIRELESS(vin, vout, iout, channel_list)
    export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")
    

# def UPDATE_VOUT_IOUT():
#     CHARGING_CURRENT = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
#     vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
#     return CHARGING_CURRENT, vout

def browning(start, end, slew, frequency):

    if start > end:
        print(f"brownout: {start} -> {end} Vac")
        for vin in np.arange(start, end+1, -slew):
            ac.voltage = vin
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)
            # CAPTURE_DATA(vin, df, excel_name)
    if start < end:
        print(f"brownin: {start} -> {end} Vac")
        for vin in np.arange(start, end+1, slew):
            ac.voltage = vin
            ac.frequency = frequency
            ac.turn_on()
            sleep(1)
            # CAPTURE_DATA(vin, df, excel_name)


def main():
    
    
    EQUIPMENT_FUNCTIONS().ELOAD_OFF(7)
    EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

    global k
    k = 0
    global df

    # creating df header list
    header_list = GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD
    for channel in channel_list:
        header_list = EQUIPMENT_FUNCTIONS().APPEND_SCOPE_LABELS(header_list, channel)
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    
    # i = 0
    # while(i < 10):
    #     CAPTURE_DATA(start, df, excel_name)
    #     sleep(1)
    #     i+=1

    # EQUIPMENT_FUNCTIONS().AC_TURN_ON(start)
    
    # i = 0
    # while(i < 30):
    #     CAPTURE_DATA(start, df, excel_name)
    #     sleep(1)
    #     i+=1

    # EQUIPMENT_FUNCTIONS().AC_TURN_ON(end)
    # i = 0
    # while(i < 30):
    #     CAPTURE_DATA(end, df, excel_name)
    #     sleep(1)
    #     i+=1

    # GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    # EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

    # sleep(1)



    browning(start, end, slew, frequency)
    input("Capture waveform")

    

if __name__ == "__main__":
 
    headers(test)
    main()
    footers(waveform_counter)
