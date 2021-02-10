# USER INPUT STARTS HERE
#########################################################################################
## TEST PARAMETERS
## set trigger settings
trigger_level = 1   # [A]
trigger_source = 2   # 
## INPUT
vin = [90,115,230,265]
freq = [60,60,50,50]

## OUTPUT
Iout_max = 3.25 # A
Iout = [Iout_max]
Iout_name = [100]
## select IC to test
# IC = 'test'
# IC = 'SEC#4 (FAB)'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
# from powi.equipment import Oscilloscope
from time import sleep, time
import os

# initialize equipment
ac = ACSource(address=5)
pms = PowerMeter(address=1)
pml = PowerMeter(address=4)
eload = ElectronicLoad(address=16)
# scope = Oscilloscope(address='10.125.10.139') # charles
scope = Oscilloscope(address='10.125.10.156') # joshua

waveform_counter = 0

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
    print()
    print(f'{waveform_counter} waveforms captured.')
    print('test complete.')
    print()
    end = time()
    total_time = end-start
    print(f'test time: {total_time:.2f} secs. / {total_time/60:.2f} mins.')

def init_trigger():
    # Trigger Settings
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope='POS')
    scope.trigger_mode(mode='NORM')
    scope.stop()

def reset():
    # print("ac.turn_off()")
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(2)
    print()

def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")




#### special functions #####

def reminders(test_name):
    print("="*50)
    print("Test Setup")
    print("="*50)
    print(f"> Load .dfl for {test_name}")
    print("> Set CH1 = Vout")
    print("> Set CH2 = Iout")
    print()
    input("Press ENTER to continue...")


def loadtransient(x=1, case="0-100", eload_channel=1, ton=0.05, toff=0.05):
    global waveform_counter

    # parse values from case
    temp = case.split("-")
    low = x*(float(temp[0])/100)
    if low == 0: low = 0
    high = x*(float(temp[1])/100)
    if high == 0: high = 0

    if low < high: trigger_slope = 'POS'
    else: trigger_slope = 'NEG'
    
    # adjust trigger level
    trigger_level = (low+high)/2
    scope.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope=trigger_slope)
    eload.channel[eload_channel].dynamic(low, high, ton, toff)
    eload.channel[eload_channel].turn_on()

    sleep(5)

    # get screenshot
    scope.run_single()
    sleep(6)
    filename = f'{voltage}Vac {frequency}Hz {case}Load.png'
    scope.get_screenshot(filename, waveforms_folder)
    print(filename)

    waveform_counter += 1


def main():

    init_trigger()

    global voltage
    global frequency

    for voltage, frequency in zip(vin, freq):

        ac.voltage = voltage
        ac.frequency = frequency
        ac.turn_on()
        # print("ac.turn_on()")
        print(f"[{voltage}Vac {frequency}Hz]")

        for x in Iout:
            # loadtransient(x, "0-25", eload_channel=1, ton=0.05, toff=0.05)
            # loadtransient(x, "25-50", eload_channel=1, ton=0.05, toff=0.05)
            # loadtransient(x, "50-75", eload_channel=1, ton=0.05, toff=0.05)
            # loadtransient(x, "75-100", eload_channel=1, ton=0.05, toff=0.05)
            loadtransient(x, "0-100", eload_channel=1, ton=0.05, toff=0.05)
            loadtransient(x, "50-100", eload_channel=1, ton=0.05, toff=0.05)
            # loadtransient(x, "100-0", eload_channel=1, ton=0.05, toff=0.05)
            # loadtransient(x, "100-50", eload_channel=1, ton=0.05, toff=0.05)
        
        reset()


## main code ##
reminders("Output Load Transient")
headers("Output Load Transient")
main()
footers()