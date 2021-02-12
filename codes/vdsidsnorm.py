# USER INPUT STARTS HERE
#########################################################################################
## TEST PARAMETERS

# comms
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.156"

# scope settings
# vin_channel = 3
# vout_channel = 1
# iout_channel = 2
# position = -2


# trigger settings
trigger_level = 10   # V
trigger_source = 2
trigger_slope = 'POS'

# eload settings
eload_channel = 1

## INPUT
vin = [90, 115, 230, 265]
freq = [60, 60, 50, 50]

## OUTPUT
vout = 20
Iout_max = 3.25 # A
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max]
Iout_name = [100, 75, 50, 25, 10, 0]
#########################################################################################
# USER INPUT ENDS HERE

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter
from time import sleep, time
import os

# initialize equipment
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

def reset():
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(1)




def percent_load():

    scope.init_trigger(trigger_source, trigger_level, trigger_slope)

    Iout_index = 0

    global waveforms_folder
    global waveform_counter
    
    waveform_counter = 0

    for voltage, frequency in zip(vin, freq):

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()

        for x in Iout:
            if x == 0:
                eload.channel[1].turn_off()
                filename = f'{voltage}Vac 0Load.png'
                sleep(2)

            else:
                eload.channel[1].cc = x
                eload.channel[1].turn_on()
                filename = f'{voltage}Vac {Iout_name[Iout_index]}LoadCC.png'
                sleep(2)
            
            # get screenshot
            scope.run_single()
            soak(6)
            filename = f'{voltage}Vac {Iout_name[Iout_index]}Load.png'
            scope.get_screenshot(filename, waveforms_folder)
            print(filename)
            Iout_index += 1
            waveform_counter += 1


            print()
        
        reset()

## main code ##
headers("Vds Ids Normal Operation")
percent_load()
footers(waveform_counter)