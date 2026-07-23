from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90,100,115,132]

soak_time = 300
soak_time_per_line = 120
soak_time_per_load = 30



# OUTPUT
iout = [1300]
led_load_list = [48,36,24]
dim_list = np.arange(0, 10.1, 0.1)
# PROJECT DETAILS
project = "DER-1021 Rev C"
test = f"Analog Dimming"
excel_name = 'test'
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():

    for led_load in led_load_list:
        input(f"Change LED load to {led_load}")

        df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_LED_LOAD[:])

        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin_list[0])

        for vin in vin_list:

            for dim in dim_list:

                EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)

                EQUIPMENT_FUNCTIONS().ANALOG_DC_ON(channel=1, voltage=dim, current=0.1)

                soak(60)

                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(vin, led_load, iout, dim, percent)

                file_name = f"{excel_name}"
                export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")

            output_list = EQUIPMENT_FUNCTIONS().BLANK_SPACE(df)
            export_to_excel(df, waveforms_folder, output_list, excel_name=file_name, sheet_name=excel_name, anchor="A1")


        i = 0

        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
        EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)

        

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)



if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)