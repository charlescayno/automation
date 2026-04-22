# @cfcayno
# date created: 11/27/2020
# last modified: 12/03/2020
# FEATURES:
#   - semi-automatic: meaning cursor from the oscilloscope needs to be change
#                     every iteration
#   - auto-capture and auto-naming of filenames
# TODO:
#   - User must load the dfl preset on the oscilloscope since
#     this code doesn't include remote oscilloscope modification
#   - PRO TIP: set trigger level to the output voltage of the test vehicle for
#              easy waveform capture
# FUTURE FEATURES:
#   - fully automatic waveform capturing

from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep, time

# USER INPUT STARTS HERE
################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1
scope_address = '10.125.10.139' #charles

# trigger settings
trigger_level = 30          # set initial trigger level
trigger_source = 3            # trigger source CHANNEL

# OUTPUT
Imax = 3
Vo = 5
Rload = int(Vo/Imax)


# ROOM TEMPERATURE

voltages = [100,115,132]
frequencies = [60,60,60]
current_name = [100]
# current = [Imax]
current_CR = [Rload]

# IC SELECTION

# IC = '25degC LAPISS2#32'
# IC = '-40degC LAPISS2#32'
# IC = '0degC LAPISS2#32'
# IC = '60degC LAPISS2#32' 

# IC = '25degC SEC#12'
# IC = '-40degC SEC#12'
# IC = '0degC SEC#12'
# IC = '60degC SEC#12' 

waveforms_folder = 'waveforms/Output Startup'
print()
print('Output Startup:')

################################################################################
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

# initialization
waveform_counter = 0

def discharge_unit():
  ac.turn_off()
  eload.channel[eload_channel].cc = 1 
  eload.channel[eload_channel].turn_on() # discharge load
  sleep(3) # discharge time

def startup_on(voltage,frequency):
  scope.run_single()
  sleep(2)
  eload.channel[eload_channel].turn_on()

  startup_90(voltage,frequency)
  input('Change cursor. Press ENTER to continue...')
  
  trigger_status = scope.trigger_status()
  return trigger_status

def startup_on_noload(voltage,frequency):
  scope.run_single()
  sleep(2)
  eload.channel[eload_channel].turn_off()

  startup_90(voltage,frequency)
  input('Change cursor. Press ENTER to continue...')
  
  trigger_status = scope.trigger_status()
  return trigger_status

def loadCC():

  current_index = 0

  for voltage, frequency in zip(voltages, frequencies):

    for x in current:

      print(f'{voltage}Vac {current_name[current_index]}LoadCC')

      eload.channel[eload_channel].cc = x
      sleep(2)
      
      startup_on(voltage,frequency)

      # get screenshot
      scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png', path=f'{waveforms_folder}')
      print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCC.png')
      print()

      discharge_unit()

      current_index = current_index + 1
      # waveform_counter = waveform_counter + 1

    # RESET current index
    current_index = 0

    discharge_unit()
    print()

  eload.channel[eload_channel].turn_off()
  print()

def loadCR():

  current_index = 0
  
  for voltage, frequency in zip(voltages, frequencies):
    
    for x in current_CR:

      print(f'{voltage}Vac {current_name[current_index]}LoadCR')

      eload.channel[eload_channel].cr = x
      sleep(2)
      
      startup_on(voltage,frequency)

      # get screenshot
      scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}LoadCR.png', path=f'{waveforms_folder}')
      print(f'{IC} {voltage}Vac {current_name[current_index]}LoadCR.png')
      print()

      discharge_unit()

      current_index = current_index + 1
      # waveform_counter = waveform_counter + 1

    # RESET current index
    current_index = 0

    discharge_unit()
    print()

  eload.channel[eload_channel].turn_off()
  print()

def noload():
  # redefine current array for no load
  current = [0]
  current_name = [0]
  current_index = 0
  waveform_counter = 0

  for voltage, frequency in zip(voltages, frequencies):
    print(f'{voltage}Vac {current_name[current_index]}Load')

    sleep(2)
    print()
    
    startup_on_noload(voltage,frequency)

    # get screenshot
    scope.get_screenshot(filename=f'{IC} {voltage}Vac {current_name[current_index]}Load.png', path=f'{waveforms_folder}')
    print(f'{IC} {voltage}Vac {current_name[current_index]}Load.png')
    print()
    current_index = 0
    # waveform_counter = waveform_counter + 1
    discharge_unit()
    print()

  eload.channel[eload_channel].turn_off()
  print()

def startup_90(voltage,frequency):
  # ac.write("OUTP:STAT?")
  # ac.write("SYST:ERR?")
  ac.voltage = 0
  ac.frequency = frequency
  # ac.write("OUTP ON")
  ac.turn_on()
  ac.write("TRIG:TRAN:SOUR BUS")
  ac.write("ABORT")
  ac.write("LIST:DWEL 1, 1, 1")
  
  ac.write("VOLT:MODE LIST")
  ac.write(f"LIST:VOLT {voltage}, {voltage}, {voltage}")
  ac.write("VOLT:SLEW:MODE LIST")
  ac.write("LIST:VOLT:SLEW 9.9e+037, 9.9e+037, 9.9e+037")
  
  ac.write("FREQ:MODE LIST")
  ac.write(f"LIST:FREQ {frequency}, {frequency}, {frequency}")
  ac.write("FREQ:SLEW:MODE LIST")
  ac.write("LIST:FREQ:SLEW 9.9e+037, 9.9e+037, 9.9e+037")

  ac.write("VOLT:OFFS:MODE FIX")
  ac.write("VOLT:OFFS:SLEW:MODE FIX")
  
  ac.write("PHAS:MODE LIST")
  ac.write("LIST:PHAS 270, 270, 270")
  
  ac.write("CURR:PEAK:MODE LIST")
  ac.write("LIST:CURR 40.4, 40.4, 40.4")
  
  ac.write("FUNC:MODE FIX")
  ac.write("LIST:TTLT ON,OFF,OFF")
  ac.write("LIST:STEP AUTO")
  # ac.write("SYST:ERR?")

  ac.write("OUTP:TTLT:STAT ON")
  ac.write("OUTP:TTLT:SOUR LIST")
  ac.write("TRIG:SYNC:SOUR PHASE")
  ac.write("TRIG:SYNC:PHAS 0.0")
  ac.write("TRIG:TRAN:DEL 0")
  ac.write("Sens:Swe:Offs:Poin 0")
  ac.write("TRIG:ACQ:SOUR TTLT")
  ac.write("INIT:IMM:SEQ3")
  ac.write("LIST:COUN 1")
  ac.write("INIT:IMM:SEQ1")
  ac.write("TRIG:TRAN:SOUR BUS")
  # ac.write("SYST:ERR?")

  ac.write("TRIG:IMM")

def startup_90_tester(voltage,frequency):
  discharge_unit()
  scope.run_single()
  sleep(2)
  startup_90(voltage,frequency)
  input("CONTINUE..")

waveform_counter = 0

print('==================== CONSTANT RESISTANCE LOAD =========================')
discharge_unit()
loadCR()


print('=======================================================================')
# print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')

