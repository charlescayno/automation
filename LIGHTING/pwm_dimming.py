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

# pwm dimming
frequency_list = [300, 3000] # Hz

# PROJECT DETAILS
project = "DER-1021"
test = f"PWM Dimming"
unit = input(">> Enter unit number: ")
excel_name = f'{project}_{test}_{unit}'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)
########################################## USER INPUT ##########################################

def main():
    

    for dim_freq in frequency_list:
        df_lowline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_PWM_DIM[:])
        df_lowline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_PWM_DIM[:])
        df_highline_LED_min = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_PWM_DIM[:])
        df_highline_LED_max = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD_PWM_DIM[:])

        for led_load in led_load_list:

            EQUIPMENT_FUNCTIONS().LED_VOLTAGE(led_load)
            EQUIPMENT_FUNCTIONS().SIG_GEN(0.001, dim_freq)

            for vin in vin_list:

                EQUIPMENT_FUNCTIONS().SIG_GEN(0.001, dim_freq)
                EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

                start_duty = 0
                end_duty = 100
                delta_duty = 1

                if start_duty < end_duty:
                    duty_list = np.arange(start_duty, end_duty+delta_duty, delta_duty)
                else: duty_list = np.arange(end_duty, start_duty-delta_duty, delta_duty)

                for duty in duty_list:

                    if duty == 0: duty = 0.01
                    EQUIPMENT_FUNCTIONS().SIG_GEN(duty, dim_freq)

                    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                    soak(3)

                    if vin <= 180:
                        if led_load == 42: 
                            a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_PWM_DIM(vin, led_load, iout, duty, dim_freq)
                            export_to_excel(df_lowline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{dim_freq}Hz_{led_load}V", anchor="A1")
                        else:
                            a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_PWM_DIM(vin, led_load, iout, duty, dim_freq)
                            export_to_excel(df_lowline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{dim_freq}Hz_{led_load}V", anchor="A1")
                    else:
                        next_anchor = 105

                        if led_load == 42: 
                            a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_PWM_DIM(vin, led_load, iout, duty, dim_freq)
                            export_to_excel(df_highline_LED_max, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{dim_freq}Hz_{led_load}V", anchor=f"A{next_anchor}")
                        else:
                            a = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_PWM_DIM(vin, led_load, iout, duty, dim_freq)
                            export_to_excel(df_highline_LED_min, waveforms_folder, a, excel_name=excel_name, sheet_name=f"{dim_freq}Hz_{led_load}V", anchor=f"A{next_anchor}")

            EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(2)

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