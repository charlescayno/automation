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

# scope_address = '10.125.10.160' #sharms
# scope_address = '10.125.10.162' #joshua
scope_address = '10.125.10.152' #charles

# TEST PARAMETERS
# trigger settings
trigger_level = 0.5329
trigger_source = 2            # channel

# INPUT
voltages = [90,265]
frequencies = [60,50]

# OUTPUT
Imax = 1.5
current = [Imax]
current_name = [100]

# IC
# IC = 'LAPISS2#35'
IC = 'SEC#11'
resistance = 'PCB end short'
# resistance = '220mOhms'
# resistance = '330mOhms'

waveforms_folder = 'waveforms/AR with Output Short/waveforms'

print()
print('AR with Output Short Test:')
print()
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
scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope.trigger_mode(mode='NORM')

# initialization
waveform_counter = 0
current_index = 0

# code for %load
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  eload.channel[eload_channel].turn_off()
  
  print(f'{IC} {voltage}Vac {resistance}')

  if resistance == 'PCB end short':
    scope.channel_position(3, -1)
    scope.channel_scale(3, 0.2)
  else:
    scope.channel_postion(3, -2)
    scope.channel_scale(3, 0.8)

  scope.run_single()
  sleep(4)
  ac.turn_on()

  input("Change cursor. Press ENTER to continue...")
  
  # get screenshot
  scope.get_screenshot(filename=f'{IC} {voltage}Vac {resistance}.png', path=f'{waveforms_folder}')
  print(f'{IC} {voltage}Vac {resistance}.png')
  
  current_index = current_index + 1
  waveform_counter = waveform_counter + 1

  # RESET current index
  current_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()

print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')