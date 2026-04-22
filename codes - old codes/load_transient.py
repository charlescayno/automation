# @cfcayno
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep, time

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address = '10.125.10.152' #charles

# trigger settings
trigger_level = 0.01          # starting trigger level
trigger_source = 2            # CH1
trigger_slope = 'NEG'

# INPUT
voltages = [100, 115, 132]
frequencies = [60, 60, 60]

# OUTPUT (DYNAMIC LOADING)
outputVoltages = [5,9,12,15,20]
Imax = [3,3.25]
ton = 0.0005
toff = 0.0005

waveforms_folder = 'waveforms/Output Load Transient'

print()
print('Output Load Transient:')

# NOTE: Load the desired dfl
#########################################################################################
# USER INPUT ENDS HERE

def setDynamicLoading():
  trigger_level = 0.5*(high-low)
  scope.trigger_level(trigger_source, trigger_level)
  eload.channel[eload_channel].dynamic(low=low, high=high, ton=ton, toff=toff)
  eload.channel[eload_channel].turn_on()
  sleep(2)

def getScreenshot():
  scope.run_single()
  sleep(5)
  scope.get_screenshot(filename=f'{voltage}Vac {vo}V {low}-{high}A.png', path=f'{waveforms_folder}')
  print(f'{voltage}Vac {vo}V {low}-{high}A.png')



start = time()
print()

# Equipment Address
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

# Trigger Settings
scope.edge_trigger(trigger_source, trigger_level, trigger_slope)
scope.trigger_mode(mode='NORM')

# initialization
waveform_counter = 0

# code for % load output ripple
for voltage, frequency in zip(voltages, frequencies):
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()

  for vo in outputVoltages:
    
    print(f'Change output voltage to {vo}V')
    input("Press ENTER to continue...")

    # set Imax depending on the output voltage
    if voltage == 20:
      curr = Imax[1] # 3.25A
    else:
      curr = Imax[0] # 3A

    # 0 - 25% Loading
    low = 0*curr
    high = 0.25*curr
    setDynamicLoading()
    getScreenshot()
    waveform_counter = waveform_counter + 1
    sleep(2)

    # # 25% - 50% Loading
    # low = 0.25*curr
    # high = 0.5*curr
    # setDynamicLoading()
    # getScreenshot()
    # waveform_counter = waveform_counter + 1
    # sleep(2)

    # # 50% - 75% Loading
    # low = 0.50*curr
    # high = 0.75*curr
    # setDynamicLoading()
    # getScreenshot()
    # waveform_counter = waveform_counter + 1
    # sleep(2)

    # # 75% - 100% Loading
    # low = 0.75*curr
    # high = curr
    # setDynamicLoading()
    # getScreenshot()
    # waveform_counter = waveform_counter + 1
    # sleep(2)

  sleep(5)

eload.channel[eload_channel].turn_off()

print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')