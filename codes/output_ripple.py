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
vin_channel = 3
vout_channel = 1
iout_channel = 2
position = -2

# trigger settings
trigger_level = 0.01   # Vrms
trigger_source = vout_channel
trigger_slope = 'POS'

# eload settings
eload_channel = 1

## INPUT
vin = [90, 115, 230, 265]
freq = [60, 60, 50, 50]

## OUTPUT
vout = 20
Iout_max = 3.25 # A
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max, 0.10*Iout_max, 0]
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

## special functions for output ripple

trigger_delta = 0.003  # [V] // describes how reactive the trigger automation
def find_trigger():
  # finding trigger level
  scope.run_single()
  soak(5)

  # get initial peak-to-peak measurement value
  labels, values = scope.get_measure()
  ptp_value = float(values[1])
  ptp_value = float(f"{ptp_value:.4f}")
  max_value = float(values[0])
  max_value = float(f"{max_value:.4f}")

  # set max_value as initial trigger level
  trigger_level = max_value
  scope.trigger_level(trigger_source, trigger_level)

  # check if it triggered within 5 seconds
  scope.run_single()
  soak(3)
  trigger_status = scope.trigger_status()

  # increase trigger level until it reaches the maximum trigger level
  while (trigger_status == 1):
    trigger_level = float(trigger_level) + trigger_delta
    scope.trigger_level(trigger_source, trigger_level)
    
    # check trigger status
    scope.run_single()
    soak(3)
    trigger_status = scope.trigger_status()

  # decrease trigger level below to get the maximum trigger possible
  trigger_level = float(trigger_level) - 2*trigger_delta
  final_trigger_level = trigger_level
  scope.trigger_level(trigger_source, trigger_level)

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
            
            find_trigger()

            # get screenshot
            scope.run_single()
            sleep(6)
            scope.get_screenshot(filename, waveforms_folder)
            print(filename)
            Iout_index += 1
            waveform_counter += 1

            reset trigger level
            scope.trigger_level(trigger_source, trigger_level = 0.010)
        
        Iout_index = 0
        print()
        reset()


## main code ##
headers("Output Ripple")
percent_load()
footers(waveform_counter)