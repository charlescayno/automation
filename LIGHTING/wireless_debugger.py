# Description: Simple EEPROM reader.
import EasyMCP2221
from time import time, sleep
from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
import struct
# Connect to MCP2221
mcp = EasyMCP2221.Device()
MEM_ADDR = 0x02
########################################## USER INPUT ##########################################
project = "DER-999"
test = "80ns_resolution"
excel_name = f"asd"
vin = 120
waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def read_eeprom():
    scope.run()
    # header_list = ["Iin (adc)", "Vbus (adc)", "CHS", "CE", "trough", "peak", "vcoil_adc", "duty_holder", "rp8",
    #                        "pin_adc", "pf_adc", "pout_adc", "eff_adc", "vin_adc",
    #                        "state", "status_if_pout_comms_received", "fod_status", "actual_vout", "actual_iout", "actual_vin"]
    # df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)

    byte_list = []
    eeprom_length = 37 # this is set by the user

    while(1):             
        data = read_eeprom_1_byte()
        decimal = hex2dec(data)
        if decimal == 1:
            byte_list.append(decimal)

            for i in range(eeprom_length-1):
                data = read_eeprom_1_byte()
                decimal = hex2dec(data)
                byte_list.append(decimal)
                # print(len(byte_list))
            
            """ EEPROM FLASH BYTES """
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

            """ ACTUAL MEASUREMENTS """
            # actual_pin = EQUIPMENT_FUNCTIONS().INPUT_POWER_POWER_METER()
            # actual_pf = EQUIPMENT_FUNCTIONS().INPUT_POWER_FACTOR_POWER_METER()
            actual_vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
            actual_iout = EQUIPMENT_FUNCTIONS().OUTPUT_CURRENT_POWER_METER()
            # actual_pout = EQUIPMENT_FUNCTIONS().OUTPUT_POWER_POWER_METER()
            # actual_iin = EQUIPMENT_FUNCTIONS().INPUT_CURRENT_POWER_METER()
            actual_vin = EQUIPMENT_FUNCTIONS().INPUT_VOLTAGE_POWER_METER()
            # try:
            #     eff_actual = actual_pout*100/actual_pin
            # except:
            #     eff_actual = "NaN"

            """ CONVERT ADC BYTES TO FLOAT """
            pin_adc = convert_from_byte([pin_byte_1, pin_byte_2, pin_byte_3, pin_byte_4])[0]
            pf_adc = convert_from_byte([pf_1, pf_2, pf_3, pf_4])[0]
            pout_adc = convert_from_byte([pout_byte_1, pout_byte_2, pout_byte_3, pout_byte_4])[0]
            eff_adc = convert_from_byte([eff_1, eff_2, eff_3, eff_4])[0]
            isense_adc = convert_from_byte([isense_msb, isense_byte1, isense_byte2, isense_lsb])[0]
            iin_adc = isense_adc_to_actual(isense_adc)
            vbus_adc = combine_bytes(vbus_msb, vbus_lsb)
            vin_adc = vbus_adc_to_actual(vbus_adc)
            vcoil_adc = combine_bytes(vcoil_msb, vcoil_lsb)      
            
            scope.stop()
            scope_measurement = scope.get_measure_dict(4)
            comms_scope_measurement = scope.get_measure_dict(1)
            # scope_measurement2 = scope.get_measure_dict(2)
            comms = EQUIPMENT_FUNCTIONS()._sigfig(comms_scope_measurement['Max'], 4)/1000
            fsw = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Frequency'], 4)/1000
            duty = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Pos. duty cycle'], 2)
            # vcoil_max = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement2['Max'], 4)
            scope.run()

            print("="*60)
            # print(f"MDC = {vin_adc}, duty = {duty} %, freq = {fsw:2f} kHz")
            resolution = 7.14 * 0.000000001
            # fsw_theo = (1 /(duty_holder*2*(resolution)))/1000
            # print(f"duty_holder = {duty_holder}, duty = {duty} %, freq = {fsw:2f} kHz, fsw_theo = {fsw_theo}")
            print()
            print(f"VbusSen = {vin_adc}, Vin (actual) = {actual_vin} Vac, Vin = {vin} Vac")
            print(f"Vbat = {actual_vout} V, Icharge = {actual_iout} A")
            print()
            # print(f"Vcoil_adc = {vcoil_adc}, Vcoil_max = {vcoil_max} V")
            # print(f"FOD Status: {fod_status}")
            print()
            print(f"CHS = {chs*100/255:.2f} %")
            print(f"CE = {ce}")
            print(f"COMMS_count = T: {trough}, P: {peak}")
            if comms > 2: print(f"COMMS STABLE")
            else: print("NO COMMS")
            if state == 1: print(f"Tx State = A-ping")
            elif state == 2: print(f"Tx State = D-ping")
            elif state == 3: print(f"Tx State = LCS")
            elif state == 4: print(f"Tx State = COMMS COUNT = 0")
            elif state == 5: print(f"Tx State = FULL CHARGE")
            elif state == 6: print(f"Tx State = FSW DECREASE (CHARGING)")
            elif state == 7: print(f"Tx State = FSW INCREASE TO REACH JITTER")
            else: print(f"Error_holder = {state}")
            print("="*60)
            print()
            print()
            print()
            
            
            # output_list = [isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8,
            #                pin_adc, pf_adc, pout_adc, eff_adc, vin_adc,
            #                state, status_if_pout_comms_received, fod_status]
            vcoil_max = 0
            output_list = [isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8,
                           pin_adc, pf_adc, pout_adc, eff_adc, vin_adc,
                           state, status_if_pout_comms_received, fod_status, actual_vout, actual_iout, actual_vin, fsw, duty, vcoil_max]

            
            # print(output_list)
            # export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="A1")
            # if vin_adc == 195: break
            # break
        byte_list=[]
    return isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8, pin_adc, pf_adc, pout_adc, eff_adc, vin_adc, state, status_if_pout_comms_received, fod_status








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

def isense_adc_to_actual(isense):
    iin = isense
    return _sigfig(iin, 4)

def vbus_adc_to_actual(vbus):
    vbulk = vbus
    return _sigfig(vbulk, 4)

def convert_from_byte(data):
    """Converts 4 bytes of data into float"""
    return [struct.unpack('<f', bytes(data[i:i+4]))[0] for i in range(0, len(data), 4)]


if __name__ == "__main__":
    headers(test)


    header_list = ["Iin (adc)", "Vbus (adc)", "CHS", "CE", "trough", "peak", "vcoil_adc", "duty_holder", "rp8",
                           "pin_adc", "pf_adc", "pout_adc", "eff_adc", "vin_adc",
                           "state", "status_if_pout_comms_received", "fod_status", "actual_vout", "actual_iout", "actual_vin", "fsw", "duty", "vcoil max"]

    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(header_list)
    EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
    soak(10)
    read_eeprom()
    # for i in range(79,133,1):
    #     EQUIPMENT_FUNCTIONS().AC_TURN_ON(i)
    #     soak(5)
    #     read_eeprom()



    footers(waveform_counter)



