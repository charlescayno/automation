# @cfcayno
# date created: 05Dec2020
# last mod.: 05Dec2020
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time
from powi.filemanager import exists
import os

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address = '10.125.10.152' #charles

# TEST PARAMETERS
# trigger settings
trigger_level = 24
trigger_source = 3            # channel

# INPUT
voltages = [90,265]
frequencies = [60,50]
# voltages = [265]
# frequencies = [50]

# OUTPUT
Imax = 1.5
# current = [Imax, 0.50*Imax]              # Amps
# current_name = [100, 50]
current = [Imax]
current_name = [100]

# IC
# IC = 'LAPISS2#35'
IC = 'SEC#11'

waveforms_folder = 'waveforms/Feedback Pin Short'

print()
print('Feedback Pin Short Circuit Protection Test:')
#########################################################################################
# USER INPUT ENDS HERE

start = time()

# Equipment Address
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

# Trigger Settings
scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='NEG')
scope.trigger_mode(mode='NORM')

# initialization
waveform_counter = 0
current_index = 0

# code for %load
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  for x in current:
    print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC')
    eload.channel[eload_channel].cc = x
    eload.channel[eload_channel].turn_on()
    sleep(5)

    scope.run_single()

    input("Change cursor. Press ENTER to continue...")
    
    # get screenshot
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png')
    
    current_index = current_index + 1
    waveform_counter = waveform_counter + 1

  # RESET current index
  current_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()

# # initialization for no-load
# current = [0]
# current_name = [0]

# input('Change Drain Current Scale. Press ENTER to continue...')

# # code for no load
# for voltage, frequency in zip(voltages, frequencies):
#   ac.voltage = voltage
#   ac.frequency = frequency
#   ac.turn_on()
  
#   eload.channel[eload_channel].turn_off()
#   sleep(5)

#   # get screenshot
#   scope.run_single()
#   sleep(6)

#   print('No Load')
#   input("Change cursor. Press ENTER to continue...")

#   scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
#   print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
  
#   current_index = current_index + 1
#   waveform_counter = waveform_counter + 1

#   current_index = 0
#   ac.turn_off()
#   sleep(5)

# eload.channel[eload_channel].turn_off()


print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')