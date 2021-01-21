# @cfcayno
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time

# Equipment Address
# ac = ACSource(address=5)
# pms = PowerMeter(address=5)
# pml = PowerMeter(address=5)
# eload = ElectronicLoad(address=5)
# scope = Oscilloscope(address='10.125.11.139')

# USER INPUT STARTS HERE
#########################################################################################
# TEST PARAMETERS
# TODO: Load the desired Output Voltage Ripple dfl
# trigger settings
trig_lvl = 0.01  # starting trigger level
trig_delta = 0.003 # [V]
trig_src = 1    # CH1
# INPUT
vin = [85, 115, 230, 265]
freq = [60, 60, 50, 50]
# OUTPUT
Iout_max = 2 # Amps
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max, 0.10*Iout_max]
Iout_name = [100, 75, 50, 25, 10]
# IC
IC = 'SEC#4'
# IC = 'LAPISS2#33'
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
  trig_lvl = max_value
  scope.trig_lvl(trig_src, trig_lvl)

  # check initial trigger status
  scope.run_single()
  sleep(5)
  trigger_status = scope.trigger_status()

  # increase trigger level until it reaches the maximum
  while (trigger_status == 1):
    trig_lvl = float(trig_lvl) + trig_delta
    scope.trig_lvl(trig_src, trig_lvl)
    
    # check trigger status
    scope.run_single()
    sleep(3)
    trigger_status = scope.trigger_status()

  # decrease one trigger level below to get the maximum trigger possible
  trig_lvl = float(trig_lvl) - 2*trig_delta
  final_trig_lvl = trig_lvl
  scope.trig_lvl(trig_src, trig_lvl)

def init_trigger():
  # Trigger Settings
  scope.edge_trigger(trig_src, trig_lvl, trigger_slope='POS')
  scope.trigger_mode(mode='NORM')
  scope.stop()

def percent_load():
  # code for % load output ripple
  for voltage, frequency in zip(vin, freq):
    ac.voltage = voltage
    ac.frequency = frequency
    ac.turn_on()
    for x in Iout:
      eload.channel[1].cc = x
      eload.channel[1].turn_on()
      
      if x == Iout[0]:
        # print('10s sleep')
        sleep(10)
      else:
        # print('5s sleep')
        sleep(5)
      
      find_trigger()

      # get screenshot
      scope.run_single()
      sleep(6)
      scope.get_screenshot(filename=f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png', path=f'{waveforms_folder}')
      print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png')
      
      Iout_index += 1
      waveform_counter += 1

      # RESET trigger level before next iteration
      trig_lvl = 0.010
      scope.trig_lvl(trig_src, trig_lvl)

    # RESET Iout index
    Iout_index = 0
    ac.turn_off()
    sleep(5)

    print()

  eload.channel[1].turn_off()







headers("Output Ripple")
# init_trigger()
print()
footers()