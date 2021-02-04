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
IC = 'SEC#4 (FAB)'
# IC = 'test'
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

def percent_load():

  init_trigger()

  global voltage
  global frequency
  for voltage, frequency in zip(vin, freq):
    
    ac.voltage = voltage
    ac.frequency = frequency
    ac.turn_on()
    
    for x in Iout:
      eload.channel[1].cc = x
      eload.channel[1].turn_on()
      
      if x == 0:
        soak(10)
      else:
        soak(5)
      
      find_trigger()
      scope.run_single()
      soak(6)
      get_screenshot()
      reset_trigger_level()
      print()
    reset()

def soak(soak_time):
  for seconds in range(soak_time, 0, -1):
      sleep(1)
      print(f"{seconds:5d}s", end="\r")
  print("       ", end="\r")

def test_line_regulation(input_list, soak_time):
  
  headers("Line Regulation")

  print("Vac, Freq, Vin, Iin, Pin, PF, %THD, Vo1, Io1, Po1, Vreg1, Eff")

  for voltage, frequency in input_list:
    ac.voltage = voltage
    ac.frequency = frequency
    ac.turn_on()

    eload.channel[1].cc = 1
    eload.channel[1].turn_on()

    soak(soak_time)

    # create output list
    vac = str(voltage)
    freq = str(frequency)
    vin = f"{pms.voltage:.2f}"
    iin = f"{pms.current*1000:.2f}"
    pin = f"{pms.power:.3f}"
    pf = f"{pms.pf:.4f}"
    thd = f"{pms.thd:.2f}"
    vo1 = f"{pml.voltage:.3f}"
    io1 = f"{pml.current*1000:.2f}"
    po1 = f"{pml.power:.3f}"
    vreg1 = f"{100*(float(vo1)-12)/12:.4f}"
    eff = f"{100*(float(po1))/float(pin):.4f}"

    output_list = [vac, freq, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]

    print(','.join(output_list))

  reset()
  footers()

## main code ##
# init_equipment()
# headers("Output Ripple")
# percent_load()
# footers()


# input_list = [(90, 60), (100, 60), (115, 60), (130, 60), (150, 60), (180, 60), (200, 50), (220, 50), (230, 50), (240, 50), (250, 60), (265, 50)]
# soak_time = 5
# test_line_regulation(input_list, soak_time)