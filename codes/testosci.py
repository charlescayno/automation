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
        global scope
        from powi.equipment import Oscilloscope
        scope = Oscilloscope(address='10.125.10.139')

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

def soak(soak_time):
        for seconds in range(soak_time, 0, -1):
                sleep(1)
                print(f"{seconds:5d}s", end="\r")
        print("       ", end="\r")

## main code ##
init_equipment()
scope.stop()
a,b = scope.get_measure(2)
print (a)
print (b)
c = scope.get_vertical(2)
print(c)
d = scope.get_horizontal()
print(d)
e = scope.get_cursor()
print(e)

print()
print()

scope.time_scale(0.0001)
scope.time_position(50)
# scope.resolution(0.1)
scope.display_intensity(100)
scope.run()
soak(1)
scope.stop()


scope.write('FORM ASC')
scope.write('EXP:WAV:INCX OFF')
data = scope.write('CHAN2:WAV1:DATA?')
print(type(data)) # string
## changing string data to list data
data = list(data.split(","))
print(len(data))
print(type(data))
temp = []
for h in data:
        h = float(h)
        h = f"{h:.4f}"
        temp.append(h)
print(len(temp))
w = 0

for i in temp:
        i = float(i)
        w+=1
        if i>0.04:
                print("@sample: " + str(w))
                break

a = scope.get_horizontal()
resolution = float(a["resolution"])
cursor1 = resolution*w
print(str(cursor1))


scope.write("CURS1:SOUR C2W1")
scope.write(f"CURS1:X1P {cursor1}")
scope.write("CURS1:X2P 0")




# print(f)