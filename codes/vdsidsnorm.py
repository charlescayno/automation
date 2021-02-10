# USER INPUT STARTS HERE
#########################################################################################
# TEST PARAMETERS

# set trigger settings
trigger_level = 0.01   # [V] starting trigger level
trigger_source = 1     # CH1
trigger_delta = 0.003  # [V] // describes how reactive the trigger automation

# INPUT
vin = [85,115,230,265]
freq = [60,60,50,50]

# OUTPUT
Iout_max = 2 # Amps
Iout = [Iout_max, 0.75*Iout_max, 0.50*Iout_max, 0.25*Iout_max]
Iout_name = [100, 75, 50, 25]

# select IC to test
IC = 'SEC#4 (FAB)'
# IC = 'test'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE
# from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from powi.equipment import Oscilloscope
from time import sleep, time
import os

# initialize equipment
# ac = ACSource(address=5)
# pms = PowerMeter(address=1)
# pml = PowerMeter(address=4)
# eload = ElectronicLoad(address=16)
scope = Oscilloscope(address='10.125.10.139') # charles
# scope = Oscilloscope(address='10.125.10.156') # joshua

# initialize variables
global Iout_index
global waveform_counter
global start
global waveforms_folder
waveform_counter = 0
Iout_index = 0

def headers(test_name):

    print()
    print("="*50)
    print(f"Test: {test_name}")

    create_folder(test_name)
    start = time()
    print()

def create_folder(test_name):
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

def percent_load():

    init_trigger()

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
            
            # get screenshot
            scope.run_single()
            soak(6)
            filename = f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png'
            scope.get_screenshot(filename, waveforms_folder)
            print(f'{IC} {voltage}Vac {Iout_name[Iout_index]}Load.png')
            Iout_index += 1
            waveform_counter += 1


            print()
        
        reset()

## main code ##
# reminders()
# headers("Vds Ids Normal Operation")
# percent_load()
# footers()