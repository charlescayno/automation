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
Vo1 = [20]
Imax1 = [2.25]

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

def load_0to25(vout2=0, iout2=0):

    input(f'Set Port B to >>> {vout2}V')
    print()

    low = 0
    high = iout2*0.25
    print(f'B: {vout2}V {iout2}A (0-25Load: {low}-{high}A)')

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
    scope.get_screenshot(filename=f'{voltage}Vac___A {vout1}V 100Load___B {vout2}V 0-25Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A {vout1}V 100Load___B {vout2}V 0-25Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_25to50(vout2=0, iout2=0):

    # input(f'Set Port B to >>> {vout2}V')
    print()

    low = iout2*0.25
    high = iout2*0.50
    print(f'B: {vout2}V {iout2}A (25-50Load: {low}-{high}A)')

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
    scope.get_screenshot(filename=f'{voltage}Vac___A {vout1}V 100Load___B {vout2}V 25-50Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A {vout1}V 100Load___B {vout2}V 25-50Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_50to75(vout2=0, iout2=0):

    # input(f'Set Port B to >>> {vout2}V')
    print()

    low = iout2*0.5
    high = iout2*0.75
    print(f'B: {vout2}V {iout2}A (50-75Load: {low}-{high}A)')

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
    scope.get_screenshot(filename=f'{voltage}Vac___A {vout1}V 100Load___B {vout2}V 50-75Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A {vout1}V 100Load___B {vout2}V 50-75Load.png')
    global waveform_counter
    waveform_counter = waveform_counter + 1

def load_75to100(vout2=0, iout2=0):

    # input(f'Set Port B to >>> {vout2}V')
    print()

    low = iout2*0.75
    high = iout2
    print(f'B: {vout2}V {iout2}A (75-100Load: {low}-{high}A)')

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
    scope.get_screenshot(filename=f'{voltage}Vac___A {vout1}V 100Load___B {vout2}V 75-100Load.png', path=f'{waveforms_folder}')
    print(f'screenshot: {voltage}Vac___A {vout1}V 100Load___B {vout2}V 75-100Load.png')
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

  for vout1, iout1 in zip(Vo1, Imax1):
    print('='*80)
    print(f'Vin = {voltage}Vac')

    print('='*80)
    input(f'Set Port A to >>> {vout1}V {iout1}A')
    eload.channel[3].cc = iout1
    eload.channel[3].turn_on()
    print(f'A: {vout1}V {iout1}A')
    print('='*80)

    for vout2, iout2 in zip(Vo2, Imax2):
      input(f"Change offset to >>> {vout2}")
      scope.channel_offset(2, {vout2})
      if vout2 == 5:
        input("Change voltage probe to x10")
      if vout2 == 5 or vout2 == 9:
        scope.channel_scale(1,1)
      elif vout2 == 12:
        input("Change voltage probe to x100.")
        scope.channel_scale(1,0.5)
      else:
        scope.channel_scale(1,0.5)
      print('-'*80)
      load_0to25(vout2, iout2)
      print('-'*80)
      load_25to50(vout2, iout2)
      print('-'*80)
      load_50to75(vout2, iout2)
      print('-'*80)
      load_75to100(vout2, iout2)

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