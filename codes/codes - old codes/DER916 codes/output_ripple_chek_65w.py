# @cfcayno
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time
# import pyautogui

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address = '10.125.10.139' #charles

# TEST PARAMETERS
# trigger settings
trigger_level = 0.01          # starting trigger level
trigger_delta = 0.003         # [V]
trigger_source = 2            # CH2

# INPUT
voltages = [100,132]
frequencies = [60,60]
# voltages = [132]
# frequencies = [60]

# OUTPUT
# port A (45W)
Vo1 = [5, 9, 12, 15, 20]
Imax1 = [3, 3, 3, 3, 2.25]
# Vo1 = [9]
# Imax1 = [3]

# port B (20W)
Vo2 = [5, 9, 12, 15, 20]
Imax2 = [3, 2.22, 1.66, 1.33, 1]

# 65W Configuration at Port B
Vo3 = [5,9, 12, 15, 20]
Imax3 = [3,3, 3, 3, 3.25]


waveforms_folder = 'waveforms/Output Ripple Waveforms'

print()
print('Output Ripple Waveforms Test:')

# NOTE: Load the desired Output Voltage Ripple dfl
#########################################################################################
# USER INPUT ENDS HERE


start = time()
print()

# Equipment Address
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

# Trigger Settings
scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope.trigger_mode(mode='NORM')
sleep(5)
scope.stop()

def find_trigger():
    
    # finding trigger level
    scope.run_single()
    sleep(5)

    # get initial peak-to-peak measurement value
    labels, values = scope.get_measure(channel=2)
    ptp_value = float(values[2])
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






# initialization
waveform_counter = 0
current_index = 0

# code for % load output ripple
for voltage, frequency in zip(voltages, frequencies):

  input(f'Remove connection on Port A.')
  print('='*80)

  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()

  for vout3, iout3 in zip(Vo3, Imax3):
    print('='*80)
    print(f'Vin = {voltage}Vac')
    
    print('='*80)
      		
    input(f'Set Port B to >>> {vout3}V')
    print(f'B: {vout3}V {iout3}A')

    eload.channel[1].cc = iout3
    eload.channel[1].turn_on()

    sleep(5)

    find_trigger()

    # get screenshot
    scope.run_single()
    sleep(6)
    
    # scope.get_screenshot(filename=f'{voltage}Vac___A (0W)___B (65W) {vout3}V 100Load.png', path=f'{waveforms_folder}')
    # print(f'{voltage}Vac___A (0W)___B (65W) {vout3}V 100Load.png')
    scope.get_screenshot(filename=f'{voltage}Vac___A (65W) {vout3}V 100Load___B (0W).png', path=f'{waveforms_folder}')
    print(f'{voltage}Vac___A (65W) {vout3}V 100Load___B (0W).png')

    eload.channel[1].turn_off()
    
    waveform_counter = waveform_counter + 1

    # RESET trigger level before next iteration
    trigger_level = 0.010
    scope.trigger_level(trigger_source, trigger_level)

    print()

ac.turn_off()
eload.channel[eload_channel].turn_off()

print()

print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')