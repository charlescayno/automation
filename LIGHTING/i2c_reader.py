# Simple EEPROM reading.
import EasyMCP2221
from time import time, sleep
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *

project = "DER-999"
test = "80ns_resolution"
excel_name = f"test"
# excel_name = f"test"
unit = "test"
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test, unit)

# Connect to MCP2221
mcp = EasyMCP2221.Device()


import matplotlib.pyplot as plt
import time
finish_counter = 0


MEM_ADDR = 0x02


def read_eeprom_1_byte():
    data = mcp.I2C_read(
        addr = MEM_ADDR,
        size = 1)
    return data

def hex2dec(data):
    decimal = int.from_bytes(data, "little")
    return decimal

def get_hex(value):
    convert_string = int(value, base=16)
    convert_hex = hex(convert_string)
    return convert_hex, convert_string

def _sigfig(number, sigfig):
        try: a = float(f"{number:.{sigfig}f}")
        except: a = "NaN"
        return a

def combine_bytes(msb, lsb):
    combined = (msb<<8) | lsb
    return combined

# def combine_bytes_float_type(byte1, byte2, byte3, byte4):
#     combined = (byte1<<24) | (byte2<<16) | (byte3<<8) | (byte4)
#     return combined

def isense_adc_to_actual(isense):
    # iin = isense*6E-4
    iin = isense
    return _sigfig(iin, 4)

def vbus_adc_to_actual(vbus):
    vbulk = vbus
    return _sigfig(vbulk, 4)

import struct

# def bytes_to_float(b1, b2, b3, b4):
#     # Combine the four bytes into a 32-bit unsigned integer in little-endian order
#     print(b1, b2, b3, b4)
#     uint_val = b1 << 24 | b2 << 16 | b3 << 8 | b4
#     # Interpret the 32-bit integer as a floating-point value
#     float_val = struct.unpack('f', struct.pack('I', uint_val))[0]
#     return float_val

def convert_from_byte(data):
    # print(data)
    return [struct.unpack('<f', bytes(data[i:i+4]))[0] for i in range(0, len(data), 4)]



# define a function to update the plot
def update_plot(ce, chs, comms_count, eff_adc, fod_status, fod_latch, max_data_points):
    global ce_data, chs_data, comms_count_data, eff_data, fod_status_data, is_it_latch_state_data
    global ax
    
    # add the new data to the lists
    ce_data.append(ce)
    chs_data.append(chs)
    comms_count_data.append(comms_count)
    eff_data.append(eff_adc)
    fod_status_data.append(fod_status)
    is_it_latch_state_data.append(fod_latch)

    # trim the lists to the maximum number of data points
    ce_data = ce_data[-max_data_points:]
    chs_data = chs_data[-max_data_points:]
    comms_count_data = comms_count_data[-max_data_points:]
    eff_data = eff_data[-max_data_points:]
    fod_status_data = fod_status_data[-max_data_points:]
    is_it_latch_state_data = is_it_latch_state_data[-max_data_points:]

    # clear the plot
    ax.clear()

    # plot the data

    # ax.plot(ce_data, label='ce')
    # ax.plot(chs_data, label='chs')
    # ax.plot(comms_count_data, label='comms_count')
    ax.plot(eff_data, label='eff')
    # ax.plot(fod_status_data, label='fod_status')
    # ax.plot(is_it_latch_state_data, label='is_it_latch')



    # set the y-axis limits
    ax.set_ylim([0, 100])


    # add a horizontal line at y=50
    ax.axhline(y=85, color='red', linestyle='--')

    # add a secondary y-axis on the right side
    ax2 = ax.twinx()
    
    # plot the data on the right y-axis
    ax2.plot(fod_status_data, marker='o', drawstyle='steps', label='fod_status', color='green')
    ax2.plot(is_it_latch_state_data,  marker='o', drawstyle='steps', label='is_it_latch', color='red')

    # set the y-axis limits for the right y-axis
    ax2.set_ylim([0, 2])

    # add the legend for the right y-axis
    ax2.legend(loc='upper right')



    # add the legend
    ax.legend()



def read_eeprom():
    global ce_data, chs_data, comms_count_data, eff_data, fod_status_data, is_it_latch_state_data, finish_counter
    global ax
    counter = 0

    # scope.run()
    
    header_list = ["Iin (ADC)", "Iin (Actual)", "Diff (%)",
                           "Vin (ADC)", "Vin (Actual)", "Diff (%)",
                           "Pin (ADC)", "Pin (Actual)", "Diff (%)",
                           "PF (ADC)", "PF (Actual)", "Diff (%)",
                           "Vout", "Iout",
                           "Pout (ADC)", "Pout (Actual)", "Diff (%)",
                           "Eff (ADC)", "Eff (Actual)", "Diff (%)",
                           "FOD Status", "CHS", "CE", "trough", "peak",
                           "Fsw"]
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    byte_list = []
    eeprom_length = 37
    iin = 0
    vbulk = 0


    # initialize the figure
    fig, ax = plt.subplots()

    # create empty lists to store the data
    ce_data = []
    chs_data = []
    comms_count_data = []
    eff_data = []
    fod_status_data = []
    is_it_latch_state_data = []


    # set the number of data points to show on the plot
    max_data_points = 100

    # set the interval between updates in seconds
    update_interval = 1

    vac_vin = 80

    while(1):
        # if counter > 5:
        #     counter == 0
        #     vac_vin += 1
        #     if vac_vin > 132: break
        #     else:
        #         EQUIPMENT_FUNCTIONS().AC_TURN_ON(vac_vin)
        #         soak(3)
                

        data = read_eeprom_1_byte()
        decimal = hex2dec(data)

        if decimal == 1:
            byte_list.append(decimal)

            for i in range(eeprom_length-1):
                data = read_eeprom_1_byte()
                decimal = hex2dec(data)
                byte_list.append(decimal)
                # print(len(byte_list))
            
            isense_msb = byte_list[3]
            isense_byte1 = byte_list[4]
            isense_byte2 = byte_list[15]
            isense_lsb = byte_list[16]
            

            vbus_msb = byte_list[5]
            vbus_lsb = byte_list[6]
            chs = byte_list[7]
            ce = byte_list[8]
            trough = byte_list[9]
            peak = byte_list[10]
            vcoil_msb = byte_list[11]
            vcoil_lsb = byte_list[12]
            duty_holder = byte_list[13]
            rp8 = byte_list[14]


            pin_byte_1 = byte_list[17]
            pin_byte_2 = byte_list[18]
            pin_byte_3 = byte_list[19]
            pin_byte_4 = byte_list[20]

            pout_byte_1 = byte_list[21]
            pout_byte_2 = byte_list[22]
            pout_byte_3 = byte_list[23]
            pout_byte_4 = byte_list[24]

            state = byte_list[25]

            status_if_pout_comms_received = byte_list[26]
            
            eff_1 = byte_list[27]
            eff_2 = byte_list[28]
            eff_3 = byte_list[29]
            eff_4 = byte_list[30]

            fod_status = byte_list[31]
            
            pf_1 = byte_list[32]
            pf_2 = byte_list[33]
            pf_3 = byte_list[34]
            pf_4 = byte_list[35]

            fod_latch = byte_list[36]


            # actual_pin = EQUIPMENT_FUNCTIONS().INPUT_POWER_POWER_METER()
            # actual_pf = EQUIPMENT_FUNCTIONS().INPUT_POWER_FACTOR_POWER_METER()
            # actual_vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
            # actual_iout = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
            # actual_pout = EQUIPMENT_FUNCTIONS().OUTPUT_POWER_POWER_METER()
            # actual_iin = EQUIPMENT_FUNCTIONS().INPUT_CURRENT_POWER_METER()
            # actual_vin = EQUIPMENT_FUNCTIONS().INPUT_VOLTAGE_POWER_METER()


            """ INPUT POWER """
            pin_adc = convert_from_byte([pin_byte_1, pin_byte_2, pin_byte_3, pin_byte_4])[0]
            

            
            """ POWER FACTOR """
            pf_adc = convert_from_byte([pf_1, pf_2, pf_3, pf_4])[0]
            
            
            """ OUTPUT POWER """
            pout_adc = convert_from_byte([pout_byte_1, pout_byte_2, pout_byte_3, pout_byte_4])[0]
            
            """ EFFICIENCY """
            eff_adc = convert_from_byte([eff_1, eff_2, eff_3, eff_4])[0]

            # try:
            #     eff_actual = actual_pout*100/actual_pin
            # except:
            #     eff_actual = "NaN"

            """ INPUT CURRENT """
            isense_adc = convert_from_byte([isense_msb, isense_byte1, isense_byte2, isense_lsb])[0]
            iin_adc = isense_adc_to_actual(isense_adc)
            
            
            """ INPUT VOLTAGE """
            vbus_adc = combine_bytes(vbus_msb, vbus_lsb)
            vin_adc = vbus_adc_to_actual(vbus_adc)
            

            """ VCOIL """
            vcoil_adc = combine_bytes(vcoil_msb, vcoil_lsb)



            
            

            # break
            # scope.stop()
            # scope_measurement = scope.get_measure_dict(4)
            # scope_measurement2 = scope.get_measure_dict(2)
            # # print(scope_measurement)
            # max_value = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Frequency'], 4)/1000
            # scope_duty = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Pos. duty cycle'], 2)
            # fsw = max_value
            # vcoil_max = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement2['Max'], 4)
            # scope.run()
            # sleep(3)

            # try:
            #     iin_diff = 100*(iin_adc/actual_iin-1)
            # except:
            #     iin_diff = 0


            # try:
            #     vin_diff = 100*(vin_adc/actual_vin-1)
            # except:
            #     vin_diff = 0

            # try:
            #     pin_diff = 100*(pin_adc/actual_pin-1)
            # except:
            #     pin_diff = 0

            # try:
            #     pf_diff = 100*(pf_adc/actual_pf-1)
            # except:
            #     pf_diff = 0

            # try:
            #     pout_diff = 100*(pout_adc/actual_pout-1)
            # except:
            #     pout_diff = 0

            
            # try:
            #     eff_diff = 100*(eff_adc/eff_actual-1)
            # except:
            #     eff_diff = 0

            
            # max_value = 1
            # output_list = [iin_adc, actual_iin, iin_diff,
            #                vin_adc, actual_vin, vin_diff,
            #                pin_adc, actual_pin, pin_diff,
            #                pf_adc, actual_pf, pf_diff,
            #                actual_vout, actual_iout, 
            #                pout_adc, actual_pout, pout_diff,
            #                eff_adc, eff_actual, eff_diff,
            #                fod_status, chs, ce, trough, peak, max_value]
            output_list = [isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8,
                           pin_adc, pf_adc, pout_adc, eff_adc, vin_adc,
                           state, status_if_pout_comms_received, fod_status]
            # output_list = [iin_adc, "NA", "NA",
            #                vin_adc, "NA", "NA",
            #                pin_adc, "NA", "NA",
            #                pf_adc, "NA", "NA",
            #                "NA", "NA", 
            #                pout_adc, "NA", "NA",
            #                eff_adc, "NA", "NA",
            #                fod_status, chs, ce, trough, peak, "NA"]
            
            # print(f"VbusSen = {vin_adc}, duty_holder = {duty_holder}, duty = {scope_duty}, freq = {fsw}")
            # print(f"Apingduty = {vin_adc}")
            # print(f"Vcoil_adc = {vcoil_adc}")
            # print(f"CHS = {chs*100/255:.2f} %")
            # print(f"CE = {ce}")
            # print(f"COMMS_count = {trough}")
            # print(output_list)
            
            # export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")


            """ PRINT """


            # try:
            #     print(f"Input Current (ADC) = {iin_adc} A")
            #     print(f"Input Current (ADC) = {iin_adc} A, Actual Input Current = {actual_iin} A, Ratio = {iin_diff} %")
            #     print(f"Input Voltage (ADC) = {vin_adc} V, Actual Input Voltage = {actual_vin} Ratio = {vin_diff} %")

            #     print(f"Pin (ADC) = {pin_adc} W, Pin (Actual) = {actual_pin} W, Ratio = {pin_diff}")
            #     print(f"PF (ADC) = {pf_adc:.4f}, PF (Actual) = {actual_pf:.4f}, Ratio = {pf_diff:.2f}")
            #     print(f"Pout (ADC) = {pout_adc} W, Pout (Actual) = {actual_pout} W, Ratio = {pout_diff}")
            #     print(f"Vout (ADC): {actual_vout:.4f} V")
            #     print(f"Eff (ADC) = {eff_adc:.2f} %, Eff (Actual) = {eff_actual:.2f}, Ratio = {eff_diff:.2f}")
            #     print(f"FOD Status: {fod_status}")
            #     print(f"CHS = {chs*100/255:.2f} %")
            #     print(f"CE = {ce}")
            #     print(f"COMMS_count = {trough+peak}")
            # except:
            #     pass
            # print(f"Is it latch state? {fod_latch}")

            print()
            print()
            break

            # update_plot(ce, chs, trough+peak, eff_adc, fod_status, fod_latch, max_data_points)
            # plt.pause(update_interval)
            # plt.show()


            # print(finish_counter)
            # if chs == 255: finish_counter += 1
            # if finish_counter > 200: break













            # sleep(1)
        byte_list=[]

        counter += 1
    return isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8, pin_adc, pf_adc, pout_adc, eff_adc, vin_adc, state, status_if_pout_comms_received, fod_status



# EQUIPMENT_FUNCTIONS().AC_TURN_ON(120)
# sleep(3)

read_eeprom()