# @cfcayno
# date created: 09Dec2020
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address = '10.125.10.139' # charles

# trigger settings
trigger_level = 0.100 # default
trigger_source = 1  # output current

# INPUT
voltages = [100, 132]
frequencies = [60, 60]

# OUTPUT
# port A (45W)
# Vo1 = [5, 9, 12, 15, 20]
# Imax1 = [3, 3, 3, 3, 2.25]
Vo1 = [15]
Imax1 = [3]

# port B (20W)
Vo2 = [5, 9, 12, 15, 20]
Imax2 = [3, 2.22, 1.66, 1.33, 1]
current2 = [0, 0.25*Imax2[0], 0.5*Imax2[0], 0.75*Imax2[0], Imax2[0]]

waveforms_folder = 'waveforms/Output Load Transient'

print()
print('Output Load Transient:')
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

# initialize counters
waveform_counter = 0
current_index = 0



for voltage, frequency in zip(voltages, frequencies):
  
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()

  eload.channel[1].dynamic(0, 1, 0.05, 0.05)
  
  eload.channel[1].turn_on()

  input()

  





ac.turn_off()  
eload.channel[eload_channel].turn_off()


print()
print('='*100)
print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')
























# for x in current:
  #   e
  #   sleep(5)

  #   # get screenshot
  #   scope.run_single()
  #   sleep(6)
  #   scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
  #   print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png')
    
  #   current_index = current_index + 1
  #   waveform_counter = waveform_counter + 1

  # # RESET current index
  # current_index = 0
  # ac.turn_off()
  # sleep(5)



# # initialization for no-load
# current = [0]
# current_name = [0]


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

#   scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
#   print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
  
#   current_index = current_index + 1
#   waveform_counter = waveform_counter + 1

#   current_index = 0
#   ac.turn_off()
#   sleep(5)

# eload.channel[eload_channel].turn_off()