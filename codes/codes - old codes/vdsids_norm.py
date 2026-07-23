# @cfcayno
# last mod.: 01Dec2020
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time
import os

# Equipment Address
# ac = ACSource(address=5)
# pms = PowerMeter(address=5)
# pml = PowerMeter(address=5)
# eload = ElectronicLoad(address=5)
# eload_channel = 1
# scope = Oscilloscope(address='10.125.11.139')

# USER INPUT STARTS HERE
#########################################################################################
# trigger settings
trigger_level = 0.21549       # V
trigger_source = 2            # channel
trigger_delta = 0.003  # [V] // describes how reactive the trigger automation

# INPUT
vin = [90,115,230,265]
frequencies = [60,60,50,50]

# OUTPUT
Iout_max = 1.5
Iout = [Iout_max, 0.50*Iout_max]              # Amps
Iout_name = [100, 50]

# IC
IC = 'SEC#4 (FAB)'
# IC = 'LAPISS2#33 (CTRL)'

waveforms_folder = 'waveforms/Vds Ids Normal Operation'
# waveforms_folder = 'waveforms/BPP Normal Operation'
# waveforms_folder = 'waveforms/BPS Normal Operation'
# waveforms_folder = 'waveforms/BPP Normal Operation'
# waveforms_folder = 'waveforms/SR FET Pin Drive Voltage'

print()
print('Vds Ids Normal Operation:')
#########################################################################################
# USER INPUT ENDS HERE
def headers(test_name):
  print()
  print("="*50)
  print(f"Test: {test_name}")
  
  global waveforms_folder
  global waveform_counter
  global Iout_index
  global start
  
  # initialization
  waveform_counter = 0
  Iout_index = 0

  waveforms_folder = f'waveforms/{test_name}'

  # creating folder for the saved waveforms
  pathname = f"{os.getcwd()}\{waveforms_folder}"
  isExist = os.path.exists(pathname)

  if isExist == False:
    os.mkdir(pathname)
    print(f"{waveforms_folder} created.")
  else:
    print(f"{waveforms_folder} folder already exists.")

  start = time()
  print()

def footers():
  print(f'{waveform_counter} waveforms captured.')
  print('test complete.')
  end = time()
  print()
  print(f'test time: {(end-start)/60} mins.')

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
    trigger_level = float(trigger_level) + trig_delta
    scope.trigger_level(trigger_source, trigger_level)
    
    # check trigger status
    scope.run_single()
    sleep(3)
    trigger_status = scope.trigger_status()

  # decrease one trigger level below to get the maximum trigger possible
  trigger_level = float(trigger_level) - 2*trig_delta
  final_trigger_level = trigger_level
  scope.trigger_level(trigger_source, trigger_level)

def init_trigger():
  # Trigger Settings
  scope.edge_trigger(trigger_source, trigger_level, trigger_slope='POS')
  scope.trigger_mode(mode='NORM')
  scope.stop()




## main code ##
headers("Output Ripple")
# init_trigger()
footers()







# code for %load
for voltage, frequency in zip(vin, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  for x in Iout:
    eload.channel[eload_channel].cc = x
    eload.channel[eload_channel].turn_on()
    sleep(5)

    # get screenshot
    scope.run_single()
    sleep(6)
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {Iout_name[Iout_index]}LoadCC.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}LoadCC.png')
    
    Iout_index = Iout_index + 1
    waveform_counter = waveform_counter + 1

  # RESET Iout index
  Iout_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()

# initialization for no-load
Iout = [0]
Iout_name = [0]


# code for no load
for voltage, frequency in zip(vin, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  
  eload.channel[eload_channel].turn_off()
  sleep(5)

  # get screenshot
  scope.run_single()
  sleep(6)

  scope.get_screenshot(filename=f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png', path=f'{waveforms_folder}')
  print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png')
  
  Iout_index = Iout_index + 1
  waveform_counter = waveform_counter + 1

  Iout_index = 0
  ac.turn_off()
  sleep(5)

eload.channel[eload_channel].turn_off()


print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')