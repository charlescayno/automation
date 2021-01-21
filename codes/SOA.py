# @cfcayno
# date created: 05Dec2020
# last mod.: 05Dec2020
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address = '10.125.10.152' #charles

# TEST PARAMETERS
trigger_level = 0.29221      # trigger level for output startup
trigger_level = 0.1269       # trigger level for output short
trigger_source = 2           # channel

# INPUT
voltages = [300]
frequencies = [50]

# OUTPUT
Imax = 1.5
# room temp
current = [Imax]
# current_name = [100]
# test = 'Output Startup'
# test = 'Output Short'

# IC
# IC = 'SEC#15 -40C'
# IC = 'SEC#15 +25C'
# IC = 'SEC#15 +100C'

# waveforms_folder = 'waveforms/SOA/waveforms/Output Short'

print()
print('SOA Test:')
#########################################################################################
# USER INPUT ENDS HERE

def discharge_unit():
  ac.turn_off()
  eload.channel[eload_channel].cc = 1 
  eload.channel[eload_channel].turn_on() # discharge load
  sleep(2) # discharge time

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

discharge_unit()

# code for %load
print()
print('==================== CONSTANT CURRENT LOAD ============================')
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  
  for x in current:
    eload.channel[eload_channel].cc = x
    eload.channel[eload_channel].turn_on()

    print(f'{IC} {voltage}Vac {test}')

    scope.run_single()

    sleep(5)

    ac.turn_on()
    
    input("Find maximum pulse limit. Press ENTER to continue...")

    sleep(2)

    scope.get_screenshot(filename=f'{IC} {voltage}Vac {test}.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {test}.png')
    
    current_index = current_index + 1
    waveform_counter = waveform_counter + 1

    print()
    discharge_unit()

  # RESET current index (for naming)
  current_index = 0 

discharge_unit()
eload.channel[eload_channel].turn_off()

input("Get SOA waveform .bin file. Press ENTER to continue...")

print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')