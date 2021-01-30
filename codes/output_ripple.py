# @cfcayno
# last mod: 22Jan2021
# from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time
import os

# Equipment Address
# ac = ACSource(address=5)
# pms = PowerMeter(address=1)
# pm1 = PowerMeter(address=1)
# pml = PowerMeter(address=4)
# pm2 = PowerMeter(address=4)
# eload = ElectronicLoad(address=16)
# scope = Oscilloscope(address='10.125.10.139')

# USER INPUT STARTS HERE
#########################################################################################
# TEST PARAMETERS
# TODO: Load the desired Output Voltage Ripple dfl
# set trigger settings
trigger_level = 0.01     # [V] starting trigger level
trigger_source = 1        # CH1
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
  # scope.run_single()
  # sleep(6)
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
  # ac.turn_off()
  # eload.channel[1].cc = 1
  # eload.channel[1].turn_on()
  # eload.channel[2].cc = 1
  # eload.channel[2].turn_on()
  sleep(5)
  print()

def percent_load():

  # init_trigger()

  global voltage
  global frequency
  for voltage, frequency in zip(vin, freq):
    
    # ac.voltage = voltage
    # ac.frequency = frequency
    # ac.turn_on()
    
    for x in Iout:
      # eload.channel[1].cc = x
      # eload.channel[1].turn_on()
      
      # if x == 0:
      #   sleep(10)
      # else:
      #   sleep(5)
      
      # find_trigger()
      # scope.run_single()
      # sleep(6)
      # get_screenshot()
      # reset_trigger_level()
      print()
    reset()


def test():
  # print("hello")
  # labels, values = scope.get_measure()
  # print(labels)
  # print(values)

  # result = scope.get_measure_all()
  # print(type(result))
  
  # print(result[0])
  # print(type(result[0]))

  # dictio = result[0]
  # print(type(dictio))

  # print(result[0]['channel'])

  scope.stop()
  # # scope.run()
  sleep(2)
  # scope.query_ascii_values('FORM ')
  data = scope.save_channel_data(1)
  print(data)




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
    vin = f"{pm1.voltage:.2f}"
    iin = f"{pm1.current*1000:.2f}"
    pin = f"{pm1.power:.3f}"
    pf = f"{pm1.pf:.4f}"
    thd = f"{pm1.thd:.2f}"
    vo1 = f"{pm2.voltage:.3f}"
    io1 = f"{pm2.current*1000:.2f}"
    po1 = f"{pm2.power:.3f}"
    vreg1 = f"{100*(float(vo1)-12)/12:.4f}"
    eff = f"{100*(float(po1))/float(pin):.4f}"

    output_list = [vac, freq, vin, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]

    print(','.join(output_list))

  reset()
  footers()





## main code ##
# headers("Output Ripple")
# percent_load()
# footers()


# test()
# test_line_regulation([(90, 60), (100, 60), (115, 60), (130, 60), (150, 60), (180, 60), (200, 50), (220, 50), (230, 50), (240, 50), (250, 60), (265, 50)],
#     soak_time = 5,
# )

soak(5)














# git config --unset credential.helper
