# @cfcayno
# date created: 11/27/2020
# FEATURES:
#   - semi-automatic waveform capture feature
#       - set the oscilloscope before capturing it via screenshot
#   - fix trigger setup
#   - 
# TODO:
#   - User must load the dfl preset on the oscilloscope since
#     this code doesn't include remote oscilloscope modification

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate, find_trigger
from time import sleep, time


# USER INPUT STARTS HERE
############################################################################################################################################################
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
trigger_level = 1.6          # set initial trigger level
trigger_source = 3            # trigger source CHANNEL

# INPUT
# voltages = [90,265]
# frequencies = [60,50]
voltages = [265]
frequencies = [50]

# OUTPUT
Imax = 1.5
Vo = 30
Rload = int(Vo/Imax)

# current_name = [50]
current_name = [100]
# current = [Imax, 0.75*Imax, 0.50*Imax, 0.25*Imax]
# current_CR = [Rload, int(Rload/0.50)]
current_CR = [Rload]
# current_CR = [int(Rload/0.50)]

# IC
# IC = 'C24'
IC = 'SEC#11_4' 

# waveforms_folder = 'waveforms/Output Startup'
waveforms_folder = 'waveforms/BPS Startup Operation'
print()
print('BPS Startup Operation:')


############################################################################################################################################################
# USER INPUT ENDS HERE
trigger_status = 0
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
# scope.trigger_level(trigger_source, trigger_level)

# initialization
waveform_counter = 0

def discharge_unit():
  ac.turn_off()
  eload.channel[eload_channel].cc = 1 
  eload.channel[eload_channel].turn_on() # discharge load
  sleep(3) # discharge time

def startup_on():
  scope.run_single()
  sleep(2)
  eload.channel[eload_channel].turn_on()
  ac.turn_on()
  sleep(3) 
  trigger_status = scope.trigger_status()
  return trigger_status

def startup_on_noload():
  scope.run_single()
  sleep(2)
  eload.channel[eload_channel].turn_off()
  ac.turn_on()
  sleep(3) 
  trigger_status = scope.trigger_status()
  return trigger_status

def loadCC():

  current_index = 0

  for voltage, frequency in zip(voltages, frequencies):
    ac.voltage = voltage
    ac.frequency = frequency
    
    for x in current:

      eload.channel[eload_channel].cc = x
      
      startup_on()

      if (trigger_status == 1):
        input("Modify cursor in oscilloscope. Press ENTER to continue screenshot capture...")
      else:
        while (trigger_status != 1):
          discharge_unit()
          input('Change trigger level on oscilloscope. Press ENTER to continue...')
          eload.channel[eload_channel].cc = x
          startup_on()


      # get screenshot
      scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
      print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png')
      
      current_index = current_index + 1
      # waveform_counter = waveform_counter + 1

    # RESET current index
    current_index = 0

    discharge_unit()

  eload.channel[eload_channel].turn_off()
  

def loadCR():
  current_index = 0
  
  for voltage, frequency in zip(voltages, frequencies):
    ac.voltage = voltage
    ac.frequency = frequency
    
    for x in current_CR:

      eload.channel[eload_channel].cr = x
      sleep(2)
      startup_on()

      print(f'{x} Ohms')
      # input("Change trigger if needed. Press ENTER to continue...")


      # get screenshot
      scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCR.png', path=f'{waveforms_folder}')
      print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCR.png')

      discharge_unit()

      current_index = current_index + 1
      # waveform_counter = waveform_counter + 1

    # RESET current index
    current_index = 0

    discharge_unit()

  

  eload.channel[eload_channel].turn_off()

def noload():
  # redefine current array for no load
  current = [0]
  current_name = [0]
  current_index = 0
  waveform_counter = 0

  for voltage, frequency in zip(voltages, frequencies):
    ac.voltage = voltage
    ac.frequency = frequency
    sleep(2)
    startup_on_noload()

    print(current[0])
    # input("Change trigger if needed. Press ENTER to continue...")

    # get screenshot
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
    
    current_index = 0
    # waveform_counter = waveform_counter + 1
    discharge_unit()

  

  eload.channel[eload_channel].turn_off()




# noload()
# loadCC()
discharge_unit()
waveform_counter = 0
loadCR()
discharge_unit()
noload()

# print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')