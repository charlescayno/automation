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
Vo1 = [5, 9, 12, 15, 20]
Imax1 = [3, 3, 3, 3, 2.25]
# Vo1 = [20]
# Imax1 = [2.25]

# port B (20W)
Vo2 = [5, 9, 12, 15, 20]
Imax2 = [3, 2.22, 1.66, 1.33, 1]

# 65W Configuration at Port B
Vo3 = [5, 9, 12, 15, 20]
Imax3 = [3, 3, 3, 3, 3.25]

waveforms_folder = 'waveforms/Output Load Transient'

print()
print('Output Load Transient:')
#########################################################################################
# USER INPUT ENDS HERE

start = time()

def load_0to25(vout3=0, iout3=0):

    input(f'Set Port B to >>> {vout3}V')
    print()

    low = 0
    high = iout3*0.25
    print(f'B: {vout3}V {iout3}A (0-25Load: {low}-{high}A)')

    eload.channel[1].dynamic(low, high, 0.05, 0.05)
    # TODO: change dynamic slope
    eload.channel[1].turn_on()

    trigger_level = (low+high)/2

    print(f'new trigger level = {trigger_level}A')
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
    sleep(2)

    scope.run_single()
    print()
    input("Press ENTER to capture screenshot...")
    scope.get_screenshot(filename=f'{voltage}Vac___A 0W___B {vout3}V 0-25Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A 0W___B {vout3}V 0-25Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_25to50(vout3=0, iout3=0):

    # input(f'Set Port B to >>> {vout3}V')
    print()

    low = iout3*0.25
    high = iout3*0.50
    print(f'B: {vout3}V {iout3}A (25-50Load: {low}-{high}A)')

    eload.channel[1].dynamic(low, high, 0.05, 0.05)
    # TODO: change dynamic slope
    eload.channel[1].turn_on()

    trigger_level = (low+high)/2

    print(f'new trigger level = {trigger_level}A')
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
    sleep(2)

    scope.run_single()
    print()
    input("Press ENTER to capture screenshot...")
    scope.get_screenshot(filename=f'{voltage}Vac___A 0W___B {vout3}V 25-50Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A 0W___B {vout3}V 25-50Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_50to75(vout3=0, iout3=0):

    # input(f'Set Port B to >>> {vout3}V')
    print()

    low = iout3*0.5
    high = iout3*0.75
    print(f'B: {vout3}V {iout3}A (50-75Load: {low}-{high}A)')

    eload.channel[1].dynamic(low, high, 0.05, 0.05)
    # TODO: change dynamic slope
    eload.channel[1].turn_on()

    trigger_level = (low+high)/2

    print(f'new trigger level = {trigger_level}A')
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
    sleep(2)

    scope.run_single()
    print()
    input("Press ENTER to capture screenshot...")
    scope.get_screenshot(filename=f'{voltage}Vac___A 0W___B {vout3}V 50-75Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A 0W___B {vout3}V 50-75Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_75to100(vout3=0, iout3=0):

    # input(f'Set Port B to >>> {vout3}V')
    print()

    low = iout3*0.75
    high = iout3
    print(f'B: {vout3}V {iout3}A (75-100Load: {low}-{high}A)')

    eload.channel[1].dynamic(low, high, 0.05, 0.05)
    # TODO: change dynamic slope
    eload.channel[1].turn_on()

    trigger_level = (low+high)/2

    print(f'new trigger level = {trigger_level}A')
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
    sleep(2)

    scope.run_single()
    print()
    input("Press ENTER to capture screenshot...")
    scope.get_screenshot(filename=f'{voltage}Vac___A 0W___B {vout3}V 75-100Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A 0W___B {vout3}V 75-100Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_transient(vout3=0, iout3=0, lowperc=0, highperc=0):
  print('-'*80)
  print()
  low = iout3*lowperc*0.01
  high = iout3*highperc*0.01
  lowperc = str(lowperc)
  highperc = str(highperc)

  print(f'B: {vout3}V {iout3}A ({lowperc[:len(lowperc)]}-{highperc[:len(highperc)]}Load: {low}-{high}A)')

  eload.channel[1].dynamic(low, high, 0.05, 0.05)
  eload.channel[1].turn_on()
  
  trigger_level = (low+high)/2
  print(f'new trigger level = {trigger_level}A')
  scope.trigger_level(trigger_source,trigger_level)
  
  sleep(2)
  scope.run_single()
  print()
  input("Press ENTER to capture screenshot...")
  filename = f"{voltage}Vac___A 0W___B {vout3}V {lowperc[:len(lowperc)]}-{highperc[:len(highperc)]}Load.png"
  path = f'{waveforms_folder}'
  scope.get_screenshot(filename=filename, path=path)
  print(f'screenshot: {voltage}Vac___A 0W___B {vout3}V {lowperc[:len(lowperc)]}-{highperc[:len(highperc)]}Load.png')
  global waveform_counter
  waveform_counter = waveform_counter + 1




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

  for vout3, iout3 in zip(Vo3, Imax3):
    print('='*80)
    print(f'Vin = {voltage}Vac')

    print('='*80)

    input(f"Change offset to >>> {vout3}")
    scope.channel_offset(2, {vout3})

    if vout3 == 5:
      input("Change voltage probe to x10")
    if vout3 == 5 or vout3 == 9:
      scope.channel_scale(1,1)
    elif vout3 == 12:
      input("Change voltage probe to x100.")
      scope.channel_scale(1,1)
    else:
      scope.channel_scale(1,1)
    
    print('-'*80)
    load_0to25(vout3, iout3)
    print('-'*80)
    load_25to50(vout3, iout3)
    print('-'*80)
    load_50to75(vout3, iout3)
    print('-'*80)
    load_75to100(vout3, iout3)
    
    load_transient(vout3, iout3, 0, 25)
    load_transient(vout3, iout3, 25, 50)
    load_transient(vout3, iout3, 50, 75)
    load_transient(vout3, iout3, 75, 100)


    eload.channel[1].turn_off()


ac.turn_off()  
eload.channel[eload_channel].turn_off()


print()
print('='*100)
print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')














