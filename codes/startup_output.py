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
scope_address = '10.125.10.152' #charles

# trigger settings
trigger_level = 30          # set initial trigger level
trigger_source = 3            # trigger source CHANNEL

# OUTPUT
Imax = 1.5
Vo = 30
Rload = int(Vo/Imax)


# ROOM TEMPERATURE

# voltages = [90,115,230,265]
# frequencies = [60,60,50,50]
# current_name = [100,50]
# current = [Imax, 0.50*Imax]
# current_CR = [Rload, int(Rload/0.50)]


# VARYING TEMPERATURE

# voltages = [90,265]
# frequencies = [60,50]
# current_name = [100]
# current = [Imax]
# current_CR = [Rload]


# w/ HIGH CAPACITANCE (3000 uF)

# voltages = [90,265]
# frequencies = [60,50]
# current_name = [100]
# current = [Imax]
# current_CR = [Rload]



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

def startup_90degPhase(voltage,frequency):
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

print('==================== CONSTANT CURRENT LOAD ============================')
discharge_unit()
loadCC()

print('==================== CONSTANT RESISTANCE LOAD =========================')
discharge_unit()
loadCR()

print('==================== NO LOAD ==========================================')
discharge_unit()
noload()

print('=======================================================================')
# print(f'{waveform_counter} waveforms captured.')
print('test complete.')

end = time()
print()
print(f'test time: {(end-start)/60} mins.')














# git config --unset credential.helper
# USER INPUT STARTS HERE
#########################################################################################
# TEST PARAMETERS
# TODO: Load the desired Output Voltage Ripple dfl
# set trigger settings
trigger_level = 0.01   # [V] starting trigger level
trigger_source = 1     # CH1
trigger_delta = 0.003  # [V] // describes how reactive the trigger automation

# INPUT
vin = [85,115,230,265]
freq = [60,60,50,50]

# OUTPUT
Iout_max = 2 # Amps
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max, 0.10*Iout_max]
Iout_name = [100, 75, 50, 25, 10]

# select IC to test
# IC = 'SEC#4 (FAB)'
IC = 'test'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE

from time import sleep, time
import os

def init_equipment():
  from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
  ac = ACSource(address=5)
  pms = PowerMeter(address=1)
  pml = PowerMeter(address=4)
  eload = ElectronicLoad(address=16)
  scope = Oscilloscope(address='10.125.10.139')

def headers(test_name):

  print()
  print("="*50)
  print(f"Test: {test_name}")
  
  # initialization
  global waveform_counter
  global Iout_index
  global start
  waveform_counter = 0
  Iout_index = 0

  create_folder(test_name)
  start = time()
  print()

def create_folder(test_name):
  global waveforms_folder
  # creating folder for the saved waveforms
  waveforms_folder = f'waveforms/{test_name}'
  pathname = f"{os.getcwd()}\{waveforms_folder}"
  isExist = os.path.exists(pathname)

  if isExist == False:
    os.mkdir(pathname)
    print(f"{waveforms_folder} created.")
  else:
    print(f"{waveforms_folder} folder already exists.")

def footers():
  print(f'{waveform_counter} waveforms captured.')
  print('test complete.')
  print()
  end = time()
  print(f'test time: {(end-start)/60} mins.')

def find_trigger():
  # finding trigger level
  scope.run_single()
  soak(5)

  # get initial peak-to-peak measurement value
  labels, values = scope.get_measure()
  ptp_value = float(values[1])
  # ptp_value = truncate(ptp_value, 4)
  ptp_value = float(f"{ptp_value:.4f}")
  max_value = float(values[0])
  # max_value = truncate(max_value, 4)
  max_value = float(f"{max_value:.4f}")

  # set max_value as initial trigger level
  trigger_level = max_value
  scope.trigger_level(trigger_source, trigger_level)

  # check initial trigger status
  scope.run_single()
  soak(5)
  trigger_status = scope.trigger_status()

  # increase trigger level until it reaches the maximum
  while (trigger_status == 1):
    trigger_level = float(trigger_level) + trigger_delta
    scope.trigger_level(trigger_source, trigger_level)
    
    # check trigger status
    scope.run_single()
    soak(3)
    trigger_status = scope.trigger_status()

  # decrease one trigger level below to get the maximum trigger possible
  trigger_level = float(trigger_level) - 2*trigger_delta
  final_trigger_level = trigger_level
  scope.trigger_level(trigger_source, trigger_level)

def init_trigger():
  # Trigger Settings
  scope.edge_trigger(trigger_source, trigger_level, trigger_slope='POS')
  scope.trigger_mode(mode='NORM')
  scope.stop()

def get_screenshot():
  global Iout_index
  global waveform_counter
  global waveforms_folder
  
  # get screenshot
  scope.run_single()
  soak(6)
  filename = f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png'
  scope.get_screenshot(filename, waveforms_folder)
  print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png')
  
  Iout_index += 1
  waveform_counter += 1

def reset_trigger_level():
  scope.trigger_level(trigger_source, trigger_level = 0.010)

def reset():
  global Iout_index
  Iout_index = 0
  ac.turn_off()
  eload.channel[1].cc = 1
  eload.channel[1].turn_on()
  eload.channel[2].cc = 1
  eload.channel[2].turn_on()
  soak(5)
  print()

def startup_cc():

  init_trigger()

  global voltage
  global frequency

  for voltage, frequency in zip(vin, freq):
    
    ac.voltage = voltage
    ac.frequency = frequency
    
    for x in Iout:
      eload.channel[1].cc = x
      eload.channel[1].turn_on()

      soak(2)

      startup_90degPhase(voltage, frequency)

      scope.run_single()
      soak(2)
      get_screenshot()

      data = scope.get_chan_data(1)
      print()

      ## search where it first happen
      j = 0
      lim = 0.8
      pos_x1 = 0
      pos_x2 = 0
      for i in data:
        if i > 120:
          pos_x1 = j
          break
        j += 1

      a = scope.get_horizontal()
      resolution = float(a["resolution"])
      minimum = float(a["scale"])*(-5)
      cursor1 = minimum + resolution*pos_x1
      cursor2 = minimum + resolution*pos_x2
      print("Y1: " + str(data[pos_x1])+ " V")
      print("X1: " + str(cursor1) + " s")
      print("Y2: " + str(data[pos_x2])+ " V")
      print("X2: " + str(cursor2) + " s")
      print()

      scope.cursor(channel=2, cursor_set=1, X1=cursor1, X2=cursor2)
      scope.cursor(channel=2, cursor_set=2, X1=cursor1, X2=cursor2)

      startup_time = scope.get_cursor()["delta x"]
      print(f"startup time = {startup_time} s")

      reset_trigger_level()
      print()
    
    reset()

def soak(soak_time):
  for seconds in range(soak_time, 0, -1):
      sleep(1)
      print(f"{seconds:5d}s", end="\r")
  print("       ", end="\r")

def startup_90degPhase(voltage,frequency):
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




## main code ##
# init_equipment()
# headers("Output Ripple")
# percent_load()
# footers()



