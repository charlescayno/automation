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
vout_channel = 1
iout_channel = 2
# position = -2

# trigger settings
trigger_level = 1   # A
trigger_source = iout_channel
trigger_slope = 'POS'

# eload settings
eload_channel = 1

## INPUT
vin = [90, 115, 230, 265]
freq = [60, 60, 50, 50]

## OUTPUT
vout = 20
Iout_max = 3.25 # A
Iout = [Iout_max, 0.50*Iout_max]
Iout_name = [100, 50]

ton = 0.001
toff = 0.001
#########################################################################################
# USER INPUT ENDS HERE

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from powi.equipment import headers, create_folder, footers, waveform_counter
from time import sleep, time
import os

## initialize equipment
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

#### special functions #####

def loadtransient(x=1, case="0-100", eload_channel=1, ton=0.05, toff=0.05):
    global waveform_counter

    # parse values from case
    temp = case.split("-")
    low = x*(float(temp[0])/100)
    if low == 0: low = 0
    high = x*(float(temp[1])/100)
    if high == 0: high = 0

    if low < high: trigger_slope = 'POS'
    else: trigger_slope = 'NEG'
    
    # adjust trigger level
    trigger_level = (low+high)/2
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope=trigger_slope)
    eload.channel[eload_channel].dynamic(low, high, ton, toff)
    eload.channel[eload_channel].turn_on()

    sleep(2)

    # get screenshot
    scope.run_single()
    sleep(6)
    filename = f'{voltage}Vac {frequency}Hz {case}Load.png'
    scope.get_screenshot(filename, waveforms_folder)
    print(filename)

    waveform_counter += 1

def main():

    scope.init_trigger(trigger_source, trigger_level, trigger_slope)

    global voltage
    global frequency

    for voltage, frequency in zip(vin, freq):

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        print(f"[{voltage}Vac {frequency}Hz]")

        for x in Iout:
            loadtransient(x, "0-100", eload_channel, ton, toff)
            loadtransient(x, "50-100", eload_channel, ton, toff)        
        reset()
        print()


## main code ##
headers("Output Load Transient")
main()
footers(waveform_counter)