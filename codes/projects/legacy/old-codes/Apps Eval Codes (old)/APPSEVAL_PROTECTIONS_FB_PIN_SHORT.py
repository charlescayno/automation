print("Charles Cayno | 07-Oct-2021")

from pyfirmata import Arduino, util
import pyfirmata
commPort = 11
board = pyfirmata.Arduino(f'COM{commPort}')
iterator = util.Iterator(board)
iterator.start()
RELAY1 = board.get_pin('d:10:o')
def relay_ON():
    RELAY1.write(1)
def relay_OFF():
    RELAY1.write(0)

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2    
eload_address = 8
scope_address = "10.125.11.0"

"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
import winsound as ws
waveform_counter = 0


"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
led = LEDControl()


"""USER INPUT"""

led_list = [46,36,24,0]
# led_list = [0]
# led_list = convert_argv_to_int_list(sys.argv[1])
# vin_list = convert_argv_to_int_list(sys.argv[2]) # [120, 230, 277] Vac
vin_list = [90,115,230,265,277,300]
# test = convert_argv_to_int_list(sys.argv[3]) # 1 - startup short, 2 - running short
# print(">> SELECT TYPE OF TEST:")
# print("1 - Startup Short")
# print("2 - Running Short")
# test = int(input("Enter type of test (1 or 2): "))
# print()
    

timeperdiv = 3

test = f"Output OVP (FB Pin Short)"
waveforms_folder = f'waveforms/{test}'

"""DEFAULT FUNCTIONS"""

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
    # print()

"""CUSTOM FUNCTIONS FOR THIS TEST"""

"""MAIN"""

print("CH1: IPRI | CH2: VR | CH3: IOUT | CH4: VOUT")

def scope_settings():

    scope.position_scale(time_position = 10, time_scale = timeperdiv) # initial setting
    scope.edge_trigger(1, 0.5, 'POS')
    scope.trigger_mode('NORM')
    scope.channel_settings(channel = 1, scale = 1, position = -4) # IDS
    scope.channel_settings(channel = 2, scale = 10, position = -3)  # VR
    scope.channel_settings(channel = 3, scale = 0.1, position = -1)   # IOUT
    scope.channel_settings(channel = 4, scale = 10, position = -2)  # VOUT


"""STARTUP SHORT"""



def startup_short():

    global waveform_counter

    scope_settings()
    
    for LED in led_list:

        led.voltage(LED)      

        discharge_output()

        for vin in vin_list:

            if LED == 0: timeperdiv = 6
            else: timeperdiv = 3
            scope.position_scale(time_position = 10, time_scale = timeperdiv)

            relay_ON()
            # input(">> Short FB Pin Short.")
            
            scope.run_single()

            sleep(1*timeperdiv)

            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            soak(10*timeperdiv)

            relay_OFF()
            # input(">> Release FB Pin Short.")
            discharge_output()
            
            prompt("Press ENTER to capture waveform")

            if LED != 0: filename = f"{vin}Vac, {LED}V, Startup FB Pin Short.png"
            else: filename = f"{vin}Vac, NL, Startup FB Pin Short.png"
            path = waveforms_folder + f'/Startup FB Pin Short'
            if not os.path.exists(path): os.mkdir(path)
            scope.get_screenshot(filename, path)
            waveform_counter += 1
            print(filename)

            print()
            # relay_OFF()
    


def running_short():

    global waveform_counter

    scope_settings()
    
    for LED in led_list:

        led.voltage(LED)      

        discharge_output()

        for vin in vin_list:

            if LED == 0: timeperdiv = 6
            else: timeperdiv = 3
            scope.position_scale(time_position = 10, time_scale = timeperdiv)
            
            scope.run_single()

            sleep(1*timeperdiv)

            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            soak(3*timeperdiv)

            relay_ON()
            # print(">> Short FB Pin Short.")

            soak(3*timeperdiv)

            relay_OFF()
            # print(">> Release FB Pin Short.")

            soak(4*timeperdiv)
            
            
            prompt("Press ENTER to capture waveform")

            if LED != 0: filename = f"{vin}Vac, {LED}V, Running FB Pin Short.png"
            else: filename = f"{vin}Vac, NL, Running FB Pin Short.png"
            path = waveforms_folder + f'/Running FB Pin Short'
            if not os.path.exists(path): os.mkdir(path)
            scope.get_screenshot(filename, path)
            waveform_counter += 1
            print(filename)

            discharge_output()

            print()





def main():
    # startup_short()
    running_short()
    


if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)
    ws.PlaySound("dingding.wav", ws.SND_ASYNC)
    sleep(2)    
