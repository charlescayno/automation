# USER INPUT STARTS HERE
#########################################################################################
## TEST PARAMETERS

# comms
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.156"

# scope settings
vin_channel = 3
vout_channel = 1
iout_channel = 2

position = -2

# trigger settings
trigger_level = 30   # Vrms
trigger_source = vin_channel
trigger_slope = 'POS'

# eload settings
eload_channel = 1

## INPUT
vin = [90, 115, 230, 265]
freq = [60, 60, 50, 50]

## OUTPUT
vout = 20
Iout_max = 3.25 # A
Iout = [Iout_max, 0.50*Iout_max]
Iout_name = [100, 50]


# typeofactivity = 'DER'
# typeofactivity = "FABXFER"

# IC = 'SEC#4 (FAB)'
# IC = 'LAPISS2#33 (CTRL)'
#########################################################################################
# USER INPUT ENDS HERE
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope
from time import sleep, time
import os

# initialize equipment
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)

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
    scope.edge_trigger(trigger_source, trigger_level, trigger_slope)
    scope.trigger_mode(mode='NORM')
    scope.stop()

def reset():
    print("resetting...")
    ac.turn_off()
    eload.channel[1].cc = 1
    eload.channel[1].turn_on()
    eload.channel[2].cc = 1
    eload.channel[2].turn_on()
    sleep(2)


def soak(soak_time):
    for seconds in range(soak_time, 0, -1):
        sleep(1)
        print(f"{seconds:5d}s", end="\r")
    print("       ", end="\r")





#### special functions #####

def reminders():
    print()
    print("Test Setup")
    print("> Load .dfl for Output Startup")
    print("> Set CH1 = Input Voltage (Diff Probe) x100 setting")
    print("> Set CH2 = Output Voltage (Barrel Probe) x10 setting")
    print("> Set CH3 = Output Current (Current Probe)")
    print()
    print("> Set position to 50%")
    scope.time_position(50)
    print("> Set the trigger level to the voltage output regulation")
    print()
    input("Press ENTER to continue...")

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
    # ac.write("LIST:PHAS 270, 270, 270")
    ac.write("LIST:PHAS 90, 90, 90")

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

def startup(case="cc"):

    global Iout_index
    global waveform_counter
    init_trigger()
    scope.trigger_level(trigger_source, trigger_level) 

    for voltage, frequency in zip(vin, freq):

        ## set input voltage
        ac.voltage = voltage
        ac.frequency = frequency

        for curr in Iout:
            if case == "cc":
                eload.channel[eload_channel].cc = curr
                eload.channel[eload_channel].turn_on()     
                filename = f'{voltage}Vac {Iout_name[Iout_index]}LoadCC.png'
            elif case == "cr":
                rload = vout/curr
                rload = f"{rload:.4f}"
                rload = float(rload)
                eload.channel[1].cr = rload
                eload.channel[eload_channel].turn_on()
                filename = f'{voltage}Vac {Iout_name[Iout_index]}LoadCR.png'
            elif case == "nl":
                eload.channel[eload_channel].turn_off()
                filename = f'{voltage}Vac 0Load.png'
            else:
                print("Please enter type of load (cc/cr/nl).")
                break

            # trigger scope
            scope.run_single()
            sleep(2)
            startup_90degPhase(voltage, frequency)
            sleep(5)
            scope.stop()

            # get waveform data from scope
            vo_data = scope.get_chan_data(vout_channel)

            # search algorithm for cursor 1
            pos_x1 = 0
            
            # search algorithm for cursor 2
            j = 0
            pos_x2 = 0
            for point in vo_data:
                if point >= vout: # if vo >= vo_reg
                    pos_x2 = j               # set cursor there
                    break
                j += 1

            # set cursors (to get startup time)
            a = scope.get_horizontal()
            resolution = float(a["resolution"])
            minimum = float(a["scale"])*(position) # set the cursor to the leftmost part of the screen
            
            if pos_x1 == 0: cursor1 = 0
            else: cursor1 = minimum + resolution*pos_x1 
            if pos_x2 == 0: cursor2 = 0
            else: cursor2 = minimum + resolution*pos_x2

            scope.cursor(channel=vin_channel, cursor_set=1, X1=cursor1, X2=cursor2)
            startup_time = scope.get_cursor()["delta x"]
            print(f"startup time = {startup_time} s")

            # get screenshot
            sleep(1)
            scope.get_screenshot(filename, waveforms_folder)
            print(filename)
            Iout_index += 1
            waveform_counter += 1

            reset()

        Iout_index = 0 # resest iout naming index for the next voltage
    print()


## main code ##
# reminders()
headers("Output Startup")
startup("cc")
startup("cr")
startup("nl")
footers()