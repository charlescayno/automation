print("CMC | 07OCT2021")
print("CHANNEL 1: IOUT")
# print("CHANNEL 2: VR")
# print("CHANNEL 3: VIN")
# print("CHANNEL 4: VOUT")

"""LIBRARIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
import winsound as ws
from playsound import playsound
waveform_counter = 0

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2    
eload_address = 8
scope_address = "10.125.11.0"

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)
# led = LEDControl()

"""USER INPUT"""

# LED = sys.argv[1] # 46, 36, 24V
led_list = [46,36,24]
# vin = convert_argv_to_int_list(sys.argv[2]) # [90, 115, 230, 265, 277, 300] Vac
vin_list = [90,115,230,277,300]
timeperdiv = 0.004 #s

# Folder Names
test = f"Iout Output Ripple"
waveforms_folder = f'waveforms/{test}'

"""DEFAULT FUNCTIONS"""

def discharge_output():
    ac.turn_off()
    for i in range(1,9):
        eload.channel[i].cc = 1
        eload.channel[i].turn_on()

    sleep(2)
    for i in range(1,9):
        eload.channel[i].turn_off()

"""CUSTOM FUNCTIONS FOR THIS TEST"""

"""MAIN"""
def main():

    global waveform_counter

    scope.time_scale(timeperdiv)
    scope.time_position(50)

    sleep(2)

    for LED in led_list:
        # led.voltage(LED)
        # prompt(f"Change LED load to {LED} Volts")
        for voltage in vin_list:
            ac.voltage = voltage
            ac.frequency = ac.set_freq(voltage)
            ac.turn_on()

            scope.run()

            prompt("Adjust cursor then press enter to continue.")

            scope.stop()

            sleep(1)
            
            filename = f"{voltage}Vac, {LED}V.png"
            scope.get_screenshot(filename, waveforms_folder)
            waveform_counter+=1
            print(filename)

            discharge_output()


if __name__ == "__main__":
    headers(test)
    discharge_output()
    main()
    discharge_output()
    footers(waveform_counter)