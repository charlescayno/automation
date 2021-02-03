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

start = time()
init_equipment()


scope.stop()
a,b = scope.get_measure(2)
print (a)
print (b)
Iout_max = float(b[0])
Iout_min = float(b[1])
c = scope.get_vertical(2)
print(c)
d = scope.get_horizontal()
print(d)
e = scope.get_cursor()
print(e)

print()
print()


# ## scope settings
# scope.time_scale(0.005)
# scope.time_position(50)
# # scope.resolution(30E-9)
# scope.display_intensity(100)

# # scope.run()
# soak(1)
# scope.stop()

# sleep(2)

data = scope.get_chan_data(2)


# with open('waveform.txt', 'w') as f:
#     for item in data:
#         f.write("%s\n" % item)

maximuminlist = max(data)
print(maximuminlist)
max_index = data.index(maximuminlist)
print(max_index)
minimuminlist = min(data)
print(minimuminlist)
min_index = data.index(minimuminlist)
print(min_index)

print()

## search where it first happen
j = 0
lim = 0.8
pos_x1 = 0
pos_x2 = 0
for i in data:
        if i == maximuminlist:
                pos_x1 = j
                print(i)
                print(pos_x1)
                break
        j += 1

j = 0
for i in data:
        if i == minimuminlist:
                pos_x2 = j
                print(i)
                print(pos_x2)
                break
        j += 1
print()

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

print()
end=time()
print(f'test time: {(end-start)} s.')

# PS C:\Users\ccayno\automation\codes> python .\testosci.py
# ['Max', 'RMS']
# ['5.691699604743e-02', '4.721091785857e-02']
# {'channel': '2', 'scale': '0.2', 'position': '-4', 'offset': '0', 'coupling': 'DCL', 'bandwidth': 'FULL'}
# {'scale': '0.0001', 'position': '0', 'resolution': '2E-09', 'sample rate': '500000000'}
# {'x1 position': '-0.000499998', 'x2 position': '0', 'y1 position': '0.71', 'y2 position': '0.89', 'delta x': '0.000499998', 'delta y': '0.18', 'source': 'C2W1'}


# Time Scale: 0.0001 s/div
# Position: 50%
# <class 'str'>
# 500000
# <class 'list'>
# 500000
# @sample: 1
# -0.000499998
# PS C:\Users\ccayno\automation\codes>


# 5Msa - 12s





# print(f)