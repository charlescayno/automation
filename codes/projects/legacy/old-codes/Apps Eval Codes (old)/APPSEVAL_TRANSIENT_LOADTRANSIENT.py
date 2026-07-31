print("Charles Cayno | 28-Sep-2021")

"""COMMS"""
ac_source_address = 9
source_power_meter_address = 2 
load_power_meter_address = 10
eload_address = 12
scope_address = "10.125.10.253"

"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list
import winsound as ws
from playsound import playsound
waveform_counter = 0

"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
# led = LEDControl()

"""TEST TITLE"""
test = f"Output Load Transient"
waveforms_folder = f'waveforms/{test}'

"""USER INPUT"""
LED = sys.argv[1] # 46, 36, 24V
vin_list = convert_argv_to_int_list(sys.argv[2]) # [120, 230, 277] Vac
transient_frequency = float(sys.argv[3]) # 500 Hz
#test_list = convert_argv_to_str_list(sys.argv[3]) # CR,CC

eload_channel = 1

# trigger settings
trigger_source = 1
trigger_level = 0
trigger_slope = 'POS'

vout = int(LED)
iout = 0.350
rload = vout/iout

iout_list = [iout, iout*0.5]
rload_list = [rload, rload*2]

ton = 1/(2*transient_frequency)
toff = ton

print(f"ton = {ton}s")
scope.position_scale(time_position = 50, time_scale = ton) # initial setting
print(f"transient frequency = {transient_frequency}Hz")
########################################################################################################
########################################################################################################
# USER INPUT ENDS HERE

def discharge_output():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    eload.channel[3].cc = 1
    eload.channel[3].turn_on()
    sleep(2)
    eload.channel[1].turn_off()
    eload.channel[2].turn_off()
    eload.channel[3].turn_off()


def scope_settings():

    # scope.position_scale(time_position = 50, time_scale = 0.05) # initial setting
    scope.edge_trigger(1, 0.5, 'POS')
    scope.trigger_mode('NORM')
    scope.channel_settings(channel = 1, scale = 0.1, position = -4) # IOUT
    scope.channel_settings(channel = 2, scale = 200, position = 2)  # VIN
    scope.channel_settings(channel = 3, scale = 0.2, position = -2)   # IDS
    scope.channel_settings(channel = 4, scale = 10, position = -2)  # VOUT

def loadtransient_cc(vin, x, case, eload_channel, ton, toff):
    global waveform_counter

    # parse values from case
    temp = case.split("-")
    
    low = x*(float(temp[0])/100)
    # print(f'Low: {low} A')
    if low == 0: low = 0
    
    high = x*(float(temp[1])/100)
    # print(f'High: {high} A')
    if high == 0: high = 0

    if low < high: trigger_slope = 'POS'
    else: trigger_slope = 'NEG'
    
    # adjust trigger level
    trigger_level = (low+high)/2
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope)
    eload.channel[eload_channel].dynamic(low, high, ton, toff)
    eload.channel[eload_channel].turn_on()

    sleep(2)

    # get screenshot
    scope.run_single()    
    
    playsound("Press ENTER to capture waveform.mp3")
    input(">> Press ENTER to capture waveform")
    vout_max = float(scope.get_cursor(4)['y1 position'])
    vout_min = float(scope.get_cursor(4)['y2 position'])
    
    # configure in case cursor is reverese
    if vout_min > vout_max:
        a = vout_max
        vout_max = vout_min
        vout_min = a

    output_list = [LED, str(vin), case, str(transient_frequency), str(vout_max), str(vout_min)]
    
    
    with open(f'{waveforms_folder}/load_transient_cc_{transient_frequency}.txt', 'a+') as f:
        f.write(','.join(output_list))
        f.write('\n')

    filename = f'{LED}V {vin}Vac {case}LoadCC {transient_frequency}Hz.png'
    scope.get_screenshot(filename, waveforms_folder)
    print(filename)
    waveform_counter += 1

def loadtransient_cr(vin, x, case, eload_channel, ton, toff):
    global waveform_counter

    # parse values from case
    temp = case.split("-")
    
    low_cr = x/(float(temp[0])/100)
    low_iout = vout / low_cr
    if low_iout == 0: low_iout = 0

    high_cr = x/(float(temp[1])/100)
    high_iout = vout / high_cr
    if high_iout == 0: high_iout = 0

    if low_iout < high_iout: trigger_slope = 'POS'
    else: trigger_slope = 'NEG'

    # adjust trigger level
    trigger_level = (low_iout+high_iout)/2
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope)

    for i in range(10):
        eload.channel[eload_channel].cr = low_cr
        eload.channel[eload_channel].turn_on()

        sleep(ton)

        eload.channel[eload_channel].cr = high_cr
        eload.channel[eload_channel].turn_on()

        sleep(toff)

        if i == 8:

            # get screenshot
            scope.run_single()    
            
    # playsound("Press ENTER to capture waveform.mp3")
    input(">> Press ENTER to capture waveform")
    vout_max = float(scope.get_cursor(4)['y1 position'])
    vout_min = float(scope.get_cursor(4)['y2 position'])
    
    # configure in case cursor is reverese
    if vout_min > vout_max:
        a = vout_max
        vout_max = vout_min
        vout_min = a

    output_list = [LED, str(vin), case, str(transient_frequency), str(vout_max), str(vout_min)]
    
    
    with open(f'{waveforms_folder}/load_transient_cr_{transient_frequency}.txt', 'a+') as f:
        f.write(','.join(output_list))
        f.write('\n')

    filename = f'{LED}V {vin}Vac {case}LoadCR {transient_frequency}Hz.png'
    scope.get_screenshot(filename, waveforms_folder)
    print(filename)
    waveform_counter += 1

    
    

    
    
    

    

def delete_file(file: str):
    filepath = f'{os.getcwd()}/{file}'
    if os.path.isfile(filepath): os.remove(filepath)

def main():

    scope_settings()
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope)
    delete_file("load_transient_cc.txt")
    delete_file("load_transient_cr.txt")
    

    for vin in vin_list:

        ac.voltage = vin
        ac.frequency = ac.set_freq(vin)
        ac.turn_on()

        print(f"[{vin}Vac {ac.set_freq(vin)}Hz]")
        
        loadtransient_cr(vin, road, "0-50", eload_channel, ton, toff)

        sleep(2)
        discharge_output()
        print()


if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)