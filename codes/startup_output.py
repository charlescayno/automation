# USER INPUT STARTS HERE
#########################################################################################
## TEST PARAMETERS
## set trigger settings
trigger_level = 20   # [V] set to the output voltage
trigger_source = 2   # CH2 = Output Voltage
## INPUT
vin = [90,115,230,265]
freq = [60,60,50,50]
## OUTPUT
Iout_max = 2 # A
Iout = [Iout_max, 0.50*Iout_max]
Iout_name = [100, 50]
## select IC to test
# IC = 'test'
# IC = 'SEC#4 (FAB)'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE

from time import sleep, time
import os

def reminders():
  print()
  print("Test Setup")
  print("> Load .dfl for Output Startup")
  print("> Set CH1 = Input Voltage (Diff Probe) x100 setting")
  print("> Set CH2 = Output Voltage (Barrel Probe) x10 setting")
  print("> Set CH3 = Output Current (Current Probe)")
  print("> Set position to 30%")
  print()
  input("Press ENTER to continue...")

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

def init_trigger():
  # Trigger Settings
  scope.edge_trigger(trigger_source, trigger_level, trigger_slope='POS')
  scope.trigger_mode(mode='NORM')
  scope.stop()

def reset():
  print("resetting...")
  ac.turn_off()
  eload.channel[1].cc = 1
  eload.channel[1].turn_on()
  eload.channel[2].cc = 1
  eload.channel[2].turn_on()
  soak(2)
  print()

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

def startup_cc():

  init_trigger()
  scope.trigger_level(trigger_source, trigger_level) 

  global voltage
  global frequency

  for voltage, frequency in zip(vin, freq):
    
    ac.voltage = voltage
    ac.frequency = frequency
    
    for x in Iout:
      eload.channel[1].cc = x
      eload.channel[1].turn_on()

      scope.run_single()
      soak(1)
      startup_90degPhase(voltage, frequency)
      soak(2)
      scope.stop()

      ####################################################

      data = scope.get_chan_data(1) # get input voltage waveform data points
      
      ## search for the time of startup
      index_ctr = 0
      lim = 126 # 127V (90*sqrt(2)=127V)
      pos_x1 = 0
      pos_x2 = 0
      for point in data:
        if point >= lim:
          pos_x1 = index_ctr
          break
        index_ctr += 1
      
      a = scope.get_horizontal()
      resolution = float(a["resolution"])
      minimum = float(a["scale"])*(-3) # set the cursor to the leftmost part of the screen
                                       # assuming position at 50%
      
      cursor1 = minimum + resolution*pos_x1
      cursor2 = pos_x2
      
      print("Y1: " + str(data[pos_x1])+ " V")
      print("X1: " + str(cursor1) + " s")
      print("Y2: " + str(data[pos_x2])+ " V")
      print("X2: " + str(cursor2) + " s")

      print()

      scope.cursor(channel=1, cursor_set=1, X1=cursor1, X2=cursor2)

      startup_time = scope.get_cursor()["delta x"]
      print(f"startup time = {startup_time} s")

      ####################################################

      filename = f'{IC} {voltage}Vac {Iout_name[Iout_index]}LoadCC.png'
      scope.get_screenshot(filename, waveforms_folder)
      print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}LoadCC.png')
      
      Iout_index += 1
      waveform_counter += 1

      print()
      reset()
    
    Iout_index = 0 # resest iout naming index for the next voltage


## main code ##
# init_equipment()
reminders()
headers("Output Startup")
# startup_cc()
footers()



