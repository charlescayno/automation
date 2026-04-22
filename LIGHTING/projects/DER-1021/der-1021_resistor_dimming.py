import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [120,230]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30

# OUTPUT
iout = 3570

led_load_list = [42, 36]
# led_load_list = [36]

# resistor dimming
resistor_list = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100] # kohms
# resistor_list = [0,1,2,3,4,5,6,7,8,9,10]


# PROJECT DETAILS
project = "DER-1021"
test = f"Resistor Dimming"
unit = input(">> Enter unit number: ")
excel_name = f'{project}_{test}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():
    df_lowline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_RESISTOR_DIM[:])
    df_lowline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_RESISTOR_DIM[:])
    df_highline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_RESISTOR_DIM[:])
    df_highline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_RESISTOR_DIM[:])

    
    for led_load in led_load_list:

        # EQUIPMENT_FUNCTIONS().LED_VOLTAGE(led_load)
        input(f"Change LED to {led_load}V")

        for resistor in resistor_list:

            input(f">> Change resistor to {resistor} kOhms.")
        
            EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

            for vin in vin_list:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                if resistor == 0: soak(30)
                soak(10)

                if vin <= 180:
                    if led_load == 42: 
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_RESISTOR_DIM(vin, led_load, iout, resistor)
                        export_to_excel(df_lowline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor="A1")
                    else:
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_RESISTOR_DIM(vin, led_load, iout, resistor)
                        export_to_excel(df_lowline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor="A1")
                else:
                    next_anchor = len(resistor_list) + 3

                    if led_load == 42: 
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_RESISTOR_DIM(vin, led_load, iout, resistor)
                        export_to_excel(df_highline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor=f"A{next_anchor}")
                    else:
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_RESISTOR_DIM(vin, led_load, iout, resistor)
                        export_to_excel(df_highline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor=f"A{next_anchor}")

            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)

        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(5)

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_lowline_LED_max)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_lowline_LED_min)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_highline_LED_max)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_highline_LED_min)

    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)