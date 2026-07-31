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

# scope_address = '10.125.10.160' #sharms
# scope_address = '10.125.10.162' #joshua
scope_address = '10.125.10.152' #charles

# TEST PARAMETERS
# trigger settings
trigger_level = 0.400       # starting trigger level
# trigger_level = 1       # starting trigger level
trigger_source = 2            # channel

# INPUT
voltages = [90,265]
frequencies = [60,50]

# OUTPUT
Imax = 1.5
# current = [Imax, 0.50*Imax]              # Amps
# current_name = [100, 50]
current = [Imax]
current_name = [100]

# IC
# IC = 'C24'
IC = 'SEC#11'

waveforms_folder = 'waveforms/BPP Normal Operation'
# waveforms_folder = 'waveforms/BPP Normal Operation'
# waveforms_folder = 'waveforms/BPS Normal Operation'
# waveforms_folder = 'waveforms/BPP Normal Operation'
# waveforms_folder = 'waveforms/SR FET Pin Drive Voltage'

print()
print('BPP Normal Operation:')
#########################################################################################
# USER INPUT ENDS HERE

def find_trigger():
    
    # finding trigger level
    scope.run_single()
    sleep(5)

    # get initial peak-to-peak measurement value
    labels, values = scope.get_measure()
    ptp_value = float(values[1])
    ptp_value = truncate(ptp_value, 4)
    max_value = float(values[0])
    max_value = truncate(max_value, 4)

    # set max_value as initial trigger level
    trigger_level = max_value
    scope.trigger_level(trigger_source, trigger_level)

    # check initial trigger status
    scope.run_single()
    sleep(5)
    trigger_status = scope.trigger_status()

    # increase trigger level until it reaches the maximum
    while (trigger_status == 1):
      trigger_level = float(trigger_level) + trigger_delta
      scope.trigger_level(trigger_source, trigger_level)
      
      # check trigger status
      scope.run_single()
      sleep(3)
      trigger_status = scope.trigger_status()

    # decrease one trigger level below to get the maximum trigger possible
    trigger_level = float(trigger_level) - 1.5*trigger_delta
    final_trigger_level = trigger_level
    scope.trigger_level(trigger_source, trigger_level)

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

input('Change Drain Current Scale. Press ENTER to continue...')

# code for %load
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  for x in current:
    eload.channel[eload_channel].cc = x
    eload.channel[eload_channel].turn_on()
    sleep(5)


    # get screenshot
    scope.run_single()
    sleep(6)

    print(f'{x} A')
    input("Change cursor. Press ENTER to continue...")
    
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png')
    
    current_index = current_index + 1
    waveform_counter = waveform_counter + 1

  # RESET current index
  current_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()

# initialization for no-load
current = [0]
current_name = [0]

input('Change Drain Current Scale. Press ENTER to continue...')

# code for no load
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  eload.channel[eload_channel].turn_off()
  sleep(5)

  # get screenshot
  scope.run_single()
  sleep(6)

  print('No Load')
  input("Change cursor. Press ENTER to continue...")

  scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
  print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
  
  current_index = current_index + 1
  waveform_counter = waveform_counter + 1

  current_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()


print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')