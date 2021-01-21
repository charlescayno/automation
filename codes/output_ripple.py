# @cfcayno
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time

# USER INPUT STARTS HERE
#########################################################################################

# TEST PARAMETERS
# trigger settings
trigger_level = 0.01          # starting trigger level
trigger_delta = 0.003         # [V]
trigger_source = 1            # CH1

# INPUT
voltages = [85, 115, 230, 265]
frequencies = [60, 60, 50, 50]

# OUTPUT
Imax = 2
current = [Imax, 0.75*Imax, 0.50*Imax, 0.25*Imax, 0.10*Imax]              # Amps
current_name = [100, 75, 50, 25, 10]

# current = [0.25*Imax]              # Amps
# current_name = [25]
# current = [0.75*Imax]              # Amps
# current_name = [75]

# IC
IC = 'SEC#4'
# IC = 'LAPISS2#33'

# NOTE: Load the desired Output Voltage Ripple dfl
#########################################################################################
# USER INPUT ENDS HERE

def headers(test_name):
  print("*"*50)
  print(f"Test: {test_name}")
  global waveforms_folder
  global waveform_counter
  global current_index
  global start
  # initialization
  waveform_counter = 0
  current_index = 0
  waveforms_folder = f'waveforms/{test_name}'
  start = time()
  print()

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
    trigger_level = float(trigger_level) - 2*trigger_delta
    final_trigger_level = trigger_level
    scope.trigger_level(trigger_source, trigger_level)

# Equipment Address
ac = ACSource(address=5)
pms = PowerMeter(address=5)
pml = PowerMeter(address=5)
eload = ElectronicLoad(address=5)
scope = Oscilloscope(address='10.125.11.139')

# Trigger Settings
scope.edge_trigger(trigger_source=1, trigger_level=0.010, trigger_slope='POS')
scope.trigger_mode(mode='NORM')
scope.stop()

headers("Output Ripple")

# code for % load output ripple
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  for x in current:
    eload.channel[1].cc = x
    eload.channel[1].turn_on()
    
    if x == current[0]:
      # print('10s sleep')
      sleep(10)
    else:
      # print('5s sleep')
      sleep(5)

    # sleep(5)

    find_trigger()

    # get screenshot
    scope.run_single()
    sleep(6)
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
    
    current_index += 1
    waveform_counter += 1

    # RESET trigger level before next iteration
    trigger_level = 0.010
    scope.trigger_level(trigger_source, trigger_level)

  # RESET current index
  current_index = 0
  ac.turn_off()
  sleep(5)

  print()

eload.channel[1].turn_off()


print()


# # initialization for no-load output ripple
# current = [0]
# current_name = [0]

# # code for no load output ripple
# for voltage, frequency in zip(voltages, frequencies):
#   ac.voltage = voltage
#   ac.frequency = frequency
#   ac.turn_on()
  
#   eload.channel[eload_channel].turn_off()
#   sleep(5)

#   find_trigger()

#   # get screenshot
#   scope.run_single()
#   sleep(6)

#   scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
#   print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
  
#   current_index = current_index + 1
#   waveform_counter = waveform_counter + 1

#   # RESET trigger level before next iteration
#   trigger_level = 0.010
#   scope.trigger_level(trigger_source, trigger_level)

#   current_index = 0
#   ac.turn_off()
#   sleep(5)




eload.channel[eload_channel].cc = 1
eload.channel[eload_channel].turn_on()

sleep(3)

eload.channel[eload_channel].turn_off()







print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')