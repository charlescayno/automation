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

# PROJECT DETAILS
project = "DER-1021"
test = f"Analog Dimming"
unit = input(">> Enter unit number: ")
excel_name = f'{project}_{test}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():

    df_lowline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD[:])
    df_lowline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD[:])
    df_highline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD[:])
    df_highline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD[:])

    for led_load in led_load_list:
        EQUIPMENT_FUNCTIONS().LED_VOLTAGE(led_load)
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        for vin in vin_list:

            start_dim_voltage = 0
            end_dim_voltage = 1
            delta_dim = 0.01

            if start_dim_voltage < end_dim_voltage:
                dim_list = np.arange(start_dim_voltage, end_dim_voltage+delta_dim, delta_dim)
            else: dim_list = np.arange(end_dim_voltage, start_dim_voltage-delta_dim, delta_dim)

            start_dim_voltage = 1
            end_dim_voltage = 10
            delta_dim = 0.1

            if start_dim_voltage < end_dim_voltage:
                dim_list_2 = np.arange(start_dim_voltage, end_dim_voltage+delta_dim, delta_dim)
            else: dim_list_2 = np.arange(end_dim_voltage, start_dim_voltage-delta_dim, delta_dim)

            dim_list_final = np.concatenate([dim_list, dim_list_2])

            for dim in dim_list_final:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
                EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=dim, current=0.1)

                if dim == 0:
                    soak(60)
                else: soak(3)

                if vin <= 180:
                    if led_load == 42: 
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, led_load, iout, dim)
                        export_to_excel(df_lowline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor="A1")
                    else:
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, led_load, iout, dim)
                        export_to_excel(df_lowline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor="A1")
                else:
                    next_anchor = 210

                    if led_load == 42: 
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, led_load, iout, dim)
                        export_to_excel(df_highline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor=f"A{next_anchor}")
                    else:
                        a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, led_load, iout, dim)
                        export_to_excel(df_highline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{led_load}V", anchor=f"A{next_anchor}")

                

        EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)


    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_lowline_LED_max)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_lowline_LED_min)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_highline_LED_max)
    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df_highline_LED_min)


if __name__ == "__main__":
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)
    headers(test)
    main()
    footers(waveform_counter)