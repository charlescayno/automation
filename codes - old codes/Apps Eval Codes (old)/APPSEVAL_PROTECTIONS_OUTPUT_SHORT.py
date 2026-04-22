print("Charles Cayno | 07-Oct-2021")




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
from playsound import playsound
waveform_counter = 0

print(">> This code is fully automated testing for startup short and running short.")
print(">> Just make sure to follow the following message below")
print(">> Make sure to connect the shorting relay to the output of the unit.")
print(">> Make sure to connect the automatic LED load control arduino setup.")
print(">> Channel settings:")
print(">> CH1: IPRI")
print(">> CH2: VR")
print(">> CH3: IOUT")
print(">> CH4: VOUT")
tts("Input IC used then press ENTER to continue")
IC = input("Input IC used: ")




"""INITIALIZE EQUIPMENT"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
led = LEDControl()

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


"""USER INPUT"""

led_list = [46,36,24,0]
# led_list = [24,0]
# led_list = [0]
vin_list = [90,115,230,265,277,300]
# vin_list = [90,300]
timeperdiv = 3

test = f"Output Short ({IC})"
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
    scope.stop()
    scope.position_scale(time_position = 10, time_scale = timeperdiv) # initial setting
    scope.edge_trigger(1, 0.5, 'POS')
    scope.trigger_mode('NORM')
    scope.channel_settings(channel = 1, scale = 1, position = -4) # IDS
    scope.channel_settings(channel = 2, scale = 10, position = -3)  # VR
    scope.channel_settings(channel = 3, scale = 0.1, position = -1)   # IOUT
    scope.channel_settings(channel = 4, scale = 10, position = -2)  # VOUT


def get_max_pin(timeperdiv):

    max_pin = 0
    for i in range(0, 10*timeperdiv, 1):
        for j in range(4):
            pin = float(f"{pms.power:.5f}")
            if max_pin < pin: max_pin = pin
            sleep(0.25)

    return max_pin

def get_max_iout(timeperdiv):

    max_iout = 0
    for i in range(0, 10*timeperdiv, 1):
        for j in range(4):
            iout = f"{pml.current:.5f}"
            iout = float(iout)*1000
            iout = f"{iout:.2f}"
            iout = float(iout)
            if max_iout < iout: max_iout = iout
            sleep(0.25)

    return max_iout


"""STARTUP SHORT"""

def startup_short():

    global waveform_counter

    scope_settings()
    
    for LED in led_list:

        led.voltage(LED)      

        discharge_output()

        for vin in vin_list:

            if LED == 0: timeperdiv = 3
            else: timeperdiv = 3
            scope.position_scale(time_position = 10, time_scale = timeperdiv)

            relay_ON()
            # playsound("short_output.mp3")
            # input(">> Short Output.")
            
            scope.run_single()

            sleep(1*timeperdiv)

            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            sleep(2)

            max_pin = get_max_pin(timeperdiv)

            discharge_output()

            if LED != 0: filename = f"{vin}Vac, {LED}V, Output Startup Short, Pin={max_pin}W.png"
            else: filename = f"{vin}Vac, NL, Output Startup Short, Pin={max_pin}W.png"
            path = waveforms_folder + f'/Output Startup Short'
            if not os.path.exists(path): os.mkdir(path)
            scope.get_screenshot(filename, path)
            waveform_counter += 1
            print(filename)


            relay_OFF()
            # playsound("remove_output_short.mp3")
            # input(">> Remove Output Short.")

            scope.run_single()

            sleep(1*timeperdiv)

            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            sleep(5)

            max_iout = get_max_iout(timeperdiv)


            discharge_output()

            if LED != 0: filename = f"{vin}Vac, {LED}V, Output Startup After Short, Iout={max_iout}mA.png"
            else: filename = f"{vin}Vac, NL, Output Startup After Short, Iout={max_iout}mA.png"
            path = waveforms_folder + f'/Output Startup Short'
            if not os.path.exists(path): os.mkdir(path)
            scope.get_screenshot(filename, path)
            waveform_counter += 1
            print(filename)

            print()
            relay_OFF()
    


def running_short(vin_list):

    global waveform_counter

    scope_settings()
    
    for LED in led_list:

        led.voltage(LED)      

        discharge_output()

        for vin in vin_list:

            if LED == 0: timeperdiv = 6
            else: timeperdiv = 3
            scope.position_scale(time_position = 20, time_scale = timeperdiv)
            

            ac.voltage = vin
            ac.frequency = ac.set_freq(vin)
            ac.turn_on()

            sleep(2*timeperdiv)

            scope.run_single()

            soak(2*timeperdiv)

            relay_ON()
            # playsound("short_output.mp3")
            # print(">> Short Output.")

            soak(4*timeperdiv)

            relay_OFF()
            # playsound("remove_output_short.mp3")
            # print(">> Remove Short.")

            soak(5*timeperdiv)
            scope.stop()

            
            prompt("Press ENTER to capture waveform")

            if LED != 0: filename = f"{vin}Vac, {LED}V, Output Running Short.png"
            else: filename = f"{vin}Vac, NL, Output Running Short.png"
            path = waveforms_folder + f'/Output Running Short'
            if not os.path.exists(path): os.mkdir(path)
            scope.get_screenshot(filename, path)
            waveform_counter += 1
            print(filename)

            discharge_output()

            # print()

def main():
    # startup_short()
    vin_list = [90,300]
    running_short(vin_list)
    
if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)
