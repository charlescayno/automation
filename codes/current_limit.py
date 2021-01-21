# @cfcayno
# last mod.: 01Dec2020
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
trigger_level = 0.200       # starting trigger level
trigger_source = 2            # channel

# INPUT
# voltages = [100,300] # DC
# voltages = [300]
voltages = [300]

# OUTPUT
Imax = 3.4
# room temp
current = [Imax, 0.50*Imax]
current_name = [100, 50]
# varying temp (remove no load test)
# current = [Imax]
# current_name = [100]

# IC
# IC = 'SEC#14'
# IC = 'LAPISS2#34'
IC = ''

# waveforms_folder = 'waveforms/Current Limit/Room Temperature'
# waveforms_folder = 'waveforms/Current Limit/-40degC'
# waveforms_folder = 'waveforms/Current Limit/0degC'
# waveforms_folder = 'waveforms/Current Limit/60degC'
waveforms_folder = 'waveforms/Current Limit'

print()
print('Current Limit Test:')
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
# discharge_unit()
# input()
# Trigger Settings
scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope.trigger_mode(mode='NORM')

# initialization
waveform_counter = 0
current_index = 0

# code for %load
print()
print('==================== CONSTANT CURRENT LOAD ============================')
for voltage in voltages:
  ac.voltage = voltage
  ac.coupling = 'DC'
  
  for x in current:
    eload.channel[eload_channel].cc = x
    eload.channel[eload_channel].turn_on()
    print(f'{voltage}Vdc {current_name[current_index]}LoadCC')
    
    # get screenshot
    scope.run_single()
    if voltage == 100 and x == current[0]:
      scope.channel_scale(trigger_source, 0.4) # 400 mA/div
    else:
      pass
    sleep(3)

    ac.turn_on()
    sleep(2)
    
    input("Find current limit. Press ENTER to continue...")

    scope.get_screenshot(filename=f'{IC} {voltage}Vdc {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vdc {current_name[current_index]}LoadCC.png')
    
    current_index = current_index + 1
    waveform_counter = waveform_counter + 1
    
    if voltage == 100 and x == current[0]:
      scope.channel_scale(trigger_source, 0.3) # 300 mA/div
    else:
      pass

    print()
    discharge_unit()

  # RESET current index
  current_index = 0
  ac.turn_off()
  discharge_unit()

eload.channel[eload_channel].turn_off()

print()
print('==================== NO LOAD ==========================================')
# initialization for no-load
current = [0]
current_name = [0]

# input('Change Drain Current Scale. Press ENTER to continue...')


# code for no load
for voltage in voltages:
  ac.voltage = voltage
  ac.coupling = 'DC'
  
  
  eload.channel[eload_channel].turn_off()
  print(f'{voltage}Vdc {current_name[current_index]}Load')
  

  # get screenshot
  scope.run_single()
  sleep(3)
  ac.turn_on()
  sleep(2)
  input("Change trigger level. Change cursor. Press ENTER to continue...")

  scope.get_screenshot(filename=f'{IC} {voltage}Vdc {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
  print(f'{IC} {voltage}Vdc {current_name[current_index]}Load.png')
  
  current_index = current_index + 1
  waveform_counter = waveform_counter + 1

  current_index = 0
  ac.turn_off()
  print()
  discharge_unit()

eload.channel[eload_channel].turn_off()


print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')