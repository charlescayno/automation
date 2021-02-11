# USER INPUT STARTS HERE
#########################################################################################
# TEST PARAMETERS

# set trigger settings
trigger_level = 0.01   # [V] starting trigger level
trigger_source = 1     # CH1
trigger_delta = 0.003  # [V] // describes how reactive the trigger automation

# INPUT
vin = [90,115,230,265]
freq = [60,60,50,50]

# OUTPUT
Iout_max = 3.25 # Amps
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max, 0]
Iout_name = [100, 75, 50, 25, 0]

# select IC to test
# IC = 'SEC#4 (FAB)'
# IC = 'test'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from powi.equipment import Oscilloscope
from time import sleep, time
import os

# initialize equipment
ac = ACSource(address=5)
pms = PowerMeter(address=1)
pml = PowerMeter(address=4)
eload = ElectronicLoad(address=16)
# scope = Oscilloscope(address='10.125.10.139') # charles
scope = Oscilloscope(address='10.125.10.156') # joshua

# initialize variables
global Iout_index
global waveform_counter
global start
global waveforms_folder
waveform_counter = 0
Iout_index = 0

def headers(test_name):
    global start
    print()
    print("="*50)
    print(f"Test: {test_name}")

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
    global start
    print(f'{waveform_counter} waveforms captured.')
    print('test complete.')
    print()
    end = time()
    print(f'test time: {(end-start)} secs.')

def init_trigger():
    # Trigger Settings
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope='POS')
    scope.trigger_mode(mode='NORM')
    scope.stop()

def reset():
    # print("resetting...")
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(1)
    print()

def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")




## special functions for output ripple

def reminders():
    print()
    print("Test Setup")
    print("> Load .dfl for Output Ripple")
    print("> Set CH1 = Output Voltage (Barrel Probe) x10 setting")
    print("Use barrel probe with filter capacitors")
    scope.time_position(50)
    input("Press ENTER to continue...")

def find_trigger():
  # finding trigger level
  scope.run_single()
  soak(5)

  # get initial peak-to-peak measurement value
  labels, values = scope.get_measure()
  ptp_value = float(values[1])
  ptp_value = float(f"{ptp_value:.4f}")
  max_value = float(values[0])
  max_value = float(f"{max_value:.4f}")

  # set max_value as initial trigger level
  trigger_level = max_value
  scope.trigger_level(trigger_source, trigger_level)

  # check if it triggered within 5 seconds
  scope.run_single()
  soak(3)
  trigger_status = scope.trigger_status()

  # increase trigger level until it reaches the maximum trigger level
  while (trigger_status == 1):
    trigger_level = float(trigger_level) + trigger_delta
    scope.trigger_level(trigger_source, trigger_level)
    
    # check trigger status
    scope.run_single()
    soak(3)
    trigger_status = scope.trigger_status()

  # decrease trigger level below to get the maximum trigger possible
  trigger_level = float(trigger_level) - 2*trigger_delta
  final_trigger_level = trigger_level
  scope.trigger_level(trigger_source, trigger_level)

def percent_load():

    init_trigger()
    Iout_index = 0

    global waveforms_folder
    global waveform_counter
    
    waveform_counter = 0

    for voltage, frequency in zip(vin, freq):

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()

        for x in Iout:
            if x == 0:
                eload.channel[1].turn_off()
                filename = f'{voltage}Vac 0Load.png'

            else:
                eload.channel[1].cc = x
                eload.channel[1].turn_on()
                filename = f'{voltage}Vac {Iout_name[Iout_index]}Load.png'
            
            if x == 0:
                soak(1)
            else:
                soak(1)
            
            find_trigger()

            # get screenshot
            scope.run_single()
            soak(6)
            scope.get_screenshot(filename, waveforms_folder)
            print(filename)
            Iout_index += 1
            waveform_counter += 1

            # reset trigger level
            scope.trigger_level(trigger_source, trigger_level = 0.010)
            print()
        
        Iout_index = 0
        reset()


## main code ##
# reminders()
headers("Output Ripple")
percent_load()
footers()